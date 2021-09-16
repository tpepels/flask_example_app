from pathlib import Path
from app import app
from flask_sqlalchemy import SQLAlchemy

Path("db").mkdir(parents=True, exist_ok=True)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db/my_app.db"
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.LargeBinary)

    def __repr__(self):
        return f"User {self.username}, {self.email}"


db.create_all()
