from app import db
from app.models import Model


class TaskList(Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    tasks = db.relationship('Task', backref='task_list', lazy=True)

    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

    def __repr__(self):
        return '<TaskList {self.id} was successfully created>'

    # Add a task to the task list
    def add_task(self, task):
        self.tasks.append(task)
        self.save()
        return self

    # Get all tasks from the task list
    def get_tasks(self):
        return self.tasks

    # Get a task from the task list
    def get_task(self, id):
        return self.tasks[id]

    # Delete a task from the task list
    def delete_task(self, id):
        self.tasks.pop(id)
        self.save()
        return self
