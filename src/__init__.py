# This file is used for creating the app with respective to its config mode so that user have some convinience
# for dev or testing or so

from flask import Flask, config, jsonify, redirect
import os
from flask.json.tag import JSONTag
from flask_jwt_extended import JWTManager
from flasgger import Swagger, swag_from

from src.auth import auth
from src.bookmarks import bookmarks
from src.database import Bookmark, db
from src.constants.http_status_codes import (
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR,
)
from src.config.swagger import template, swagger_config


def create_app(test_config=None):

    app = Flask(__name__, instance_relative_config=True)

    if test_config is None:

        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
            SWAGGER={"title": "Bookmarks API", "uiversion": 3},
        )
    else:
        app.config.from_mapping(test_config)

    # registering app database
    # after registering app and creating models we should open flask shell and create database by using db.create_all()
    db.app = app
    db.init_app(app)

    # configure JWT with app
    JWTManager(app)

    # before returning the app we need to register blue_prints
    app.register_blueprint(auth)
    app.register_blueprint(bookmarks)

    # configure swagger
    Swagger(app, config=swagger_config, template=template)

    # handle the visits count and redirecting to url
    @app.get("/<short_url>")
    @swag_from("./docs/short_url.yaml")
    def redirect_to_url(short_url):
        bookmark = Bookmark.query.filter_by(short_url=short_url).first_or_404()

        if bookmark:
            bookmark.visits += 1
            db.session.commit()

            return redirect(bookmark.url)

    # error handlers that will return json instead viewing html on web page
    @app.errorhandler(HTTP_404_NOT_FOUND)
    def handle_404(e):
        return jsonify({"error": "Not Found"}), HTTP_404_NOT_FOUND

    @app.errorhandler(HTTP_500_INTERNAL_SERVER_ERROR)
    def handle_500(e):
        return (
            jsonify({"error": "Something went wrong please try again later."}),
            HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return app
