from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash
from . import db
from .exceptions import NotFound


class Model(db.Model):
    __abstract__ = True

    # def __init__(self, **kwargs):
    #     super(Model, self).__init__(**kwargs)

    @classmethod
    def get(cls, id):
        model = cls.query.get(id)
        if model:
            return model
        raise NotFound

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def create(self):
        db.session.add(self)
        self.save()
        return self

    def save(self):
        db.session.commit()
        return self

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return self

    def to_dict(self, include=[], exclude=[]):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns if c.name not in exclude or c.name in include}


class Task(Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow())

    def __init__(self, content) -> None:
        super().__init__()
        self.content = content
        self.date_created = datetime.utcnow()

    def __repr__(self):
        return '<Task {self.id} was successfully created>'


class Account(UserMixin, Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))

    def __init__(self, email, name, password) -> None:
        super().__init__()
        self.email = email
        self.name = name
        self.password = generate_password_hash(password)
