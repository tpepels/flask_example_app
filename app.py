from flask import Flask, request, render_template, make_response

app = Flask(__name__)

from controler import hash_password, check_password, password_complexity
from model import db, User

INVALID_MESSAGE = "Invalid username or password"

# https://flask.palletsprojects.com/en/2.0.x/quickstart
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/


@app.route("/user/<user_id>")
def get_user(user_id: int):
    user = User.query.filter_by(id=user_id).first()
    if user:
        return make_response({"username": user.username, "email": user.email}, 200)
    else:
        return make_response({"error": f"User with id {user_id} does not exist"})


@app.route("/create", methods=["GET"])
def create_user_template():
    return render_template("create_user.html")


@app.route("/create", methods=["POST"])
def create_user():

    data = request.json
    print(data)

    username = request.form["username"]
    email = request.form["email"]
    password = request.form["password"]

    the_user = User.query.filter_by(username=username).first()
    if the_user is not None:
        return make_response({"error": "Please select a different username."}, 400)

    the_user = User.query.filter_by(email=email).first()
    if the_user is not None:
        return make_response({"error": "A user with this e-mail address already exists."}, 400)

    # returns a message is the password does not meet complexity standards
    if msg := password_complexity(password):
        return make_response({"error": "password does not meet complexity requirements.", "failed": msg}, 400)

    # Don't do this ^ (it puts the clear text password in the url....)
    hashed_pw = hash_password(password)
    try:
        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
    except Exception as ex:
        return make_response({"error": f"could not create user {str(ex)}"}, 400)

    return make_response({"result": "success"}, 200)


@app.route("/login", methods=["GET"])
def show_login():
    return render_template("login.html", logged_in=False)


@app.route("/login/template", methods=["POST"])
def process_login_template():
    username = request.form["username"]
    password = request.form["password"]

    # First, let's check if the user exists
    the_user = User.query.filter_by(username=username).first()
    if the_user is None:
        return render_template("login.html", logged_in=False, message=INVALID_MESSAGE)

    # Now let's compare the stored password with the given password
    if check_password(the_user, password):
        return render_template("login.html", logged_in=True, username=username)
    else:
        return render_template("login.html", logged_in=False, message=INVALID_MESSAGE)


@app.route("/login", methods=["POST"])
def process_login():
    username = request.form["username"]
    password = request.form["password"]

    # First, let's check if the user exists
    the_user = User.query.filter_by(username=username).first()
    if the_user is None:
        return INVALID_MESSAGE

    # Now let's compare the stored password with the given password
    if check_password(the_user, password):
        return make_response({"result": "Login successful"}, 200)
    else:
        return make_response({"error": INVALID_MESSAGE}, 400)
