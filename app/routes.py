from flask import Blueprint, render_template, request, redirect, url_for
import json
from . import db
from .models import Todo


routes = Blueprint('routes', __name__)


def JSONResponse(content: dict,
                 status_code: int,
                 headers: dict = {'ContentType': 'application/json'}) -> tuple:
    return json.dumps(content, default=str), status_code, headers


responses = {
    200: JSONResponse({'success': True}, 200),
    505: JSONResponse({'success': False}, 500)
}


@routes.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")


@routes.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        # code to validate and add user to database goes here
        return redirect(url_for('routes.login'))


@routes.route("/", methods=['GET'])
def home():
    if request.method == 'GET':
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("/index.html", tasks=tasks)


@routes.route('/tasks', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        tasks = Todo.query.order_by(Todo.date_created).all()
        return JSONResponse({'tasks': [task.to_dict() for task in tasks]}, 200)
    elif request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return JSONResponse({'task': new_task.to_dict()}, 200)
        except Exception:
            return responses[500]


@routes.route('/tasks/<int:id>', methods=['POST'])
def complete_task(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed

    try:
        db.session.commit()
        return responses[200]
    except Exception:
        return responses[500]


@routes.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    task = Todo.query.get_or_404(id)
    task.content = request.form['content']

    try:
        db.session.commit()
        return responses[200]
    except Exception:
        return responses[500]


@routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return responses[200]
    except Exception:
        return responses[500]
