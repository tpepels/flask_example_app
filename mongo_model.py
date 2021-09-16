from pymongo import MongoClient

# Based on the tutorial at:
# - https://www.mongodb.com/blog/post/getting-started-with-python-and-mongodb

# pprint library is used to make the output look more pretty
from pprint import pprint

# Use a separate file to store the connection string because we don't want to push this to github
from private import mongo_connection

client = MongoClient(mongo_connection)

db = client.login_data

# https://cloud.mongodb.com/


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
        kwargs["_id"] = kwargs["id"]
        kwargs.pop("id")

    result = db.user.find_one(kwargs)

    if result:
        return User.deserialize(result)

    return None


def save_new_user(username, hashed_pw, email):
    db.user.insert_one({"username": username, "email": email, "password": hashed_pw})
