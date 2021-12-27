from flask import Blueprint, request
from flask import json
from flask.json import jsonify
from flask_jwt_extended.view_decorators import verify_jwt_in_request
from flasgger import swag_from
import validators
from flask_jwt_extended import get_jwt_identity, jwt_required

from src.constants.http_status_codes import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
)
from src.database import Bookmark, db

# blueprint represents collection of routes together with some single prefix
bookmarks = Blueprint("bookmarks", __name__, url_prefix="/api/v1/bookmarks")

# base url to get and post bookmarks data
@bookmarks.route("/", methods=["POST", "GET"])
@jwt_required()
@swag_from("./docs/bookmarks/get.yaml", methods=["GET"])
@swag_from("./docs/bookmarks/post.yaml", methods=["POST"])
def handle_bookmarks():
    current_user = get_jwt_identity()
    # user bookmark post
    if request.method == "POST":
        body = request.get_json().get("body", "")
        url = request.get_json().get("url", "")
        # using validators to verify email
        if not validators.url(url):
            return jsonify({"error": "Enter a valid url"}), HTTP_400_BAD_REQUEST

        if Bookmark.query.filter_by(url=url).first():
            return jsonify({"error": "URL already exists"}), HTTP_409_CONFLICT

        bookmark = Bookmark(url=url, body=body, user_id=current_user)
        db.session.add(bookmark)
        db.session.commit()

        return (
            jsonify(
                {
                    "id": bookmark.id,
                    "url": bookmark.url,
                    "short_url": bookmark.short_url,
                    "visit": bookmark.visits,
                    "body": bookmark.body,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                }
            ),
            HTTP_201_CREATED,
        )

    else:
        # implementing pagination so that we can send requested number of links to the page in frontend
        page = request.args.get("page", 1, type=int)
        per_page = request.args.get("per_page", 5, type=int)

        current_user = get_jwt_identity()
        bookmarks = Bookmark.query.filter_by(user_id=current_user).paginate(
            page=page, per_page=per_page
        )

        data = []

        for bookmark in bookmarks.items:
            data.append(
                {
                    "id": bookmark.id,
                    "url": bookmark.url,
                    "short_url": bookmark.short_url,
                    "visits": bookmark.visits,
                    "body": bookmark.body,
                    "created_at": bookmark.created_at,
                    "updated_at": bookmark.updated_at,
                }
            )

        meta = {
            "page": bookmarks.page,
            "pages": bookmarks.pages,
            "total_count": bookmarks.total,
            "prev_page": bookmarks.prev_num,
            "next_page": bookmarks.next_num,
            "has_prev": bookmarks.has_prev,
            "has_next": bookmarks.has_next,
        }

        return jsonify({"data": data, "meta": meta}), HTTP_200_OK


# to retrieve single link using id
@bookmarks.get("/<int:id>")
@jwt_required()
@swag_from("./docs/bookmarks/get_id.yaml")
def get_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND

    return (
        {
            "id": bookmark.id,
            "url": bookmark.url,
            "short_url": bookmark.short_url,
            "visits": bookmark.visits,
            "body": bookmark.body,
            "created_at": bookmark.created_at,
            "updated_at": bookmark.updated_at,
        }
    ), HTTP_200_OK


# to delete bookmark by id
@bookmarks.delete("/<int:id>")
@jwt_required()
@swag_from("./docs/bookmarks/delete.yaml")
def delete_bookmark(id):
    current_user = get_jwt_identity()

    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND

    db.session.delete(bookmark)
    db.session.commit()

    return jsonify({}), HTTP_204_NO_CONTENT


# to edit or update bookmark by id
@bookmarks.put("/<int:id>")  # put is used for updating items of bookmarks
@bookmarks.patch("<int:id>")  # patch for updating pieces of small info in items
@jwt_required()
@swag_from("./docs/bookmarks/update.yaml")
def editbookmark(id):
    current_user = get_jwt_identity()
    # check for the existance of bookmark
    bookmark = Bookmark.query.filter_by(user_id=current_user, id=id).first()

    if not bookmark:
        return jsonify({"message": "Item not found"}), HTTP_404_NOT_FOUND
    # check if new url is valid
    url = request.get_json().get("url", "")
    body = request.get_json().get("body", "")
    if not validators.url(url):
        return jsonify({"error": "Enter a valid url"}), HTTP_400_BAD_REQUEST

    # update the retrieved bookmark url, body and commit to db
    bookmark.url = url
    bookmark.body = body

    db.session.commit()

    return (
        jsonify(
            {
                "id": bookmark.id,
                "url": bookmark.url,
                "short_url": bookmark.short_url,
                "visit": bookmark.visits,
                "body": bookmark.body,
                "created_at": bookmark.created_at,
                "updated_at": bookmark.updated_at,
            }
        ),
        HTTP_200_OK,
    )


# new route for getting stats of url in bookmarks
@bookmarks.get("/stats")
@jwt_required()
@swag_from("./docs/bookmarks/stats.yaml")
def get_stats():
    current_user = get_jwt_identity()
    data = []

    items = Bookmark.query.filter_by(user_id=current_user).all()

    for item in items:
        link_stats = {
            "visits": item.visits,
            "url": item.url,
            "id": item.id,
            "short_url": item.short_url,
        }

        data.append(link_stats)

    return (
        jsonify(
            {
                "data": data,
            }
        ),
        HTTP_200_OK,
    )
