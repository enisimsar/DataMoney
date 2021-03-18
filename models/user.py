from marshmallow_mongoengine import fields
from mongoengine import DateTimeField, DictField, IntField, StringField

from .base import BaseDocument, BaseSchema

__author__ = "Enis Simsar"


class User(BaseDocument):
    user_id = StringField(max_length=50, required=True, unique=True)
    entry = DictField(required=True)
    meta = {
        "collection": "users",
        "index_background": True,
        "auto_create_index": True,
        "indexes": ["user_id"],
    }

    def schema(self):
        return UserSchema()


class UserSchema(BaseSchema):
    class Meta:
        model = User


class UserConnection(BaseDocument):
    follower_id = StringField(max_length=50, required=True)
    user_id = StringField(max_length=50, required=True, unique_with="follower_id")
    meta = {
        "collection": "user_connections",
        "index_background": True,
        "auto_create_index": True,
        "indexes": ["user_id", "follower_id"],
    }

    def schema(self):
        return UserConnectionSchema()


class UserConnectionSchema(BaseSchema):
    class Meta:
        model = UserConnection


class UserMentions(BaseDocument):
    from_id = StringField(max_length=50, required=True)
    mention_id = StringField(max_length=50, required=True, unique_with="from_id")
    user_id = StringField(max_length=50, required=True)
    published_at = DateTimeField(required=True)
    meta = {
        "collection": "user_mentions",
        "index_background": True,
        "auto_create_index": True,
        "indexes": ["user_id", "mention_id", "from_id"],
    }

    def schema(self):
        return UserConnectionSchema()


class UserMentionsSchema(BaseSchema):
    class Meta:
        model = UserMentions
