# Based on the tutorial at:
# - https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb
from pymongo import MongoClient

# https://api.mongodb.com/python/2.8/tutorial.html#getting-a-single-document-with-find-one
from bson.objectid import ObjectId


# Use a separate file to store the connection string because we don't want to push this to github
from private import mongo_connection

# I'm using a hosted mongodb instance (free up to 500MB)
# https://cloud.mongodb.com/
client = MongoClient(mongo_connection)

db = client.login_data


class User:
    def __init__(self, _id: str, username: str, email: str, password: bytearray):
        self.id = _id
        self.username = username
        self.email = email
        self.password = password

    @staticmethod
    def deserialize(user_d: dict):
        return User(**user_d)

    def __repr__(self):
        return f"User {self.username}, {self.email}"


def find_single_user(**kwargs):
    if "id" in kwargs:
        kwargs["_id"] = ObjectId(kwargs["id"])
        kwargs.pop("id")

    print(kwargs)
    result = db.user.find_one(kwargs)

    if result:
        return User.deserialize(result)

    return None


def save_new_user(username, hashed_pw, email):
    db.user.insert_one({"username": username, "email": email, "password": hashed_pw})
