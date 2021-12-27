# imports for creating models
from enum import unique
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import string, random

# creating sql db
db = SQLAlchemy()

# creating db models by inheriting Model class from db

# User class/tabe for auth with bookmarks as foreign key
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())
    bookmarks = db.relationship("Bookmark", backref="user")

    def __repr__(self) -> str:
        return "User>>> {self.username}"


# bookmark class/table, as user as foreign key connected
class Bookmark(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text, nullable=False)
    url = db.Column(db.Text, nullable=False)
    short_url = db.Column(db.String(3), nullable=False)
    visits = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    created_at = db.Column(db.DateTime, default=datetime.now())
    updated_at = db.Column(db.DateTime, onupdate=datetime.now())

    # generating short 3 letter chars that include alpha numerics for shortening url
    def generate_short_characters(self):
        characters = string.digits + string.ascii_letters
        picked_chars = "".join(random.choices(characters, k=3))

        # check if picked characters already exists
        link = self.query.filter_by(short_url=picked_chars).first()

        if link:
            self.generate_short_characters()  # until we get some unique url
        else:
            return picked_chars

    # constructor class called default when model called
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

        self.short_url = self.generate_short_characters()

    def __repr__(self) -> str:
        return "Bookmark>>> {self.url}"
