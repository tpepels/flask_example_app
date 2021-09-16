# -*- coding: utf-8 -*-
from PyInquirer import prompt
import requests

BASE_URL = "http://localhost:5000"

main_list = {
    "type": "list",
    "name": "choice",
    "message": "What do you want to do?",
    "choices": ["Create a user", "Login", "Get a user", "Quit"],
}


login_questions = [
    {"type": "input", "message": "Enter your username", "name": "username"},
    {"type": "password", "message": "Enter your password", "name": "password"},
]

create_questions = login_questions + [
    {"type": "input", "message": "Enter your e-mail address", "name": "email"},
]

user_id_questions = [
    {"type": "input", "message": "Enter the id", "name": "user_id"},
]


def login(username, password):
    response = requests.post(BASE_URL + "/login", data={"username": username, "password": password})
    print(response.json())


def create(username, password, email):
    response = requests.post(BASE_URL + "/create", data={"username": username, "password": password, "email": email})
    print(response.json())


def get_user(user_id):
    response = requests.get(BASE_URL + "/user/" + user_id)
    print(response.json())


if __name__ == "__main__":
    while True:
        answers = prompt(main_list)
        answer = answers["choice"]
        if answer == "Create a user":
            create_answers = prompt(create_questions)
            create(**create_answers)
        if answer == "Login":
            login_answers = prompt(login_questions)
            login(**login_answers)
        if answer == "Get a user":
            get_user_answers = prompt(user_id_questions)
            get_user(**get_user_answers)
        if answer == "Quit":
            break
