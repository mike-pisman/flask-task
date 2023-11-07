from datetime import datetime

from app import db
from app.models import Model


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