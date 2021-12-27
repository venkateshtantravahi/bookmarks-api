from os import access
from flasgger import swag_from
from flask import Blueprint, request
from flask.json import jsonify
from flask_jwt_extended.utils import get_jwt_identity
from werkzeug.security import check_password_hash, generate_password_hash
import validators
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_409_CONFLICT,
)
from src.database import User, db

# blueprint represents collection of routes together with some single prefix
auth = Blueprint("auth", __name__, url_prefix="/api/v1/auth")

# route for user registration
@auth.post("/register")
@swag_from("./docs/auth/register.yaml")
def register():
    # parsing values from request
    username = request.json["username"]
    email = request.json["email"]
    password = request.json["password"]

    if len(password) < 6:
        # checking len of password matches our criteria
        return jsonify({"error": "Paasowrd is too short"}), HTTP_400_BAD_REQUEST

    if len(username) < 3:
        return jsonify({"error": "Paasowrd is too short"}), HTTP_400_BAD_REQUEST

    if not username.isalnum() or " " in username:
        return (
            jsonify({"error": "Username should be alphanumeric , also no spaces"}),
            HTTP_400_BAD_REQUEST,
        )

    # using validators for validating userdata
    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    # checking existance of email in Users model
    if User.query.filter_by(email=email).first() is not None:
        return jsonify({"error": "Email already exists"}), HTTP_409_CONFLICT

    # checking existance of username in Users model
    if User.query.filter_by(username=username).first() is not None:
        return jsonify({"error": "Username already exists"}), HTTP_409_CONFLICT

    # hash password and save in db
    pwd_hash = generate_password_hash(password)
    user = User(username=username, password=pwd_hash, email=email)
    db.session.add(user)
    db.session.commit()

    return (
        jsonify(
            {"message": "User Created", "user": {"username": username, "email": email}}
        ),
        HTTP_201_CREATED,
    )


# route for user login
@auth.post("/login")
@swag_from("./docs/auth/login.yaml")
def login():
    email = request.json.get(
        "email", ""
    )  # extra empty char for handling if no email passed, so that app doesn't crashes
    password = request.json.get("password", "")

    user = User.query.filter_by(email=email).first()
    if user:
        is_pass_correct = check_password_hash(user.password, password)

        if is_pass_correct:
            refresh = create_refresh_token(identity=user.id)
            access = create_access_token(identity=user.id)

            return (
                jsonify(
                    {
                        "user": {
                            "refresh": refresh,
                            "access": access,
                            "username": user.username,
                            "email": user.email,
                        }
                    }
                ),
                HTTP_200_OK,
            )

    return jsonify({"error": "Wrong Credentials"}), HTTP_401_UNAUTHORIZED


# when an endpoint needs user authentication we can make use of jwt_required api
@auth.get("/me")
@jwt_required()
def me():
    user_id = get_jwt_identity()

    user = User.query.filter_by(id=user_id).first()

    return jsonify({"username": user.username, "email": user.email}), HTTP_200_OK


# handling user refresh
@auth.get("/token/refresh")
@jwt_required(refresh=True)
@swag_from("./docs/auth/refresh.yaml")
def refresh_user_token():
    identity = get_jwt_identity()
    access = create_access_token(identity=identity)

    return (
        {
            "access": access,
        }
    ), HTTP_200_OK
