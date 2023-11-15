from app import db
from app.models import Model
from flask_login import UserMixin
from werkzeug.security import generate_password_hash


class Account(UserMixin, Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(200))
    name = db.Column(db.String(100))
    lists = db.relationship('TaskList', backref='account', lazy=True)

    def __init__(self, email, name, password) -> None:
        super().__init__()
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
