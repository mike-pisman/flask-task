from flask import Blueprint, render_template, request, redirect, url_for
import json
from .models import Task
from .exceptions import NotFound

routes = Blueprint('routes', __name__)


def JSONResponse(content: dict,
                 status_code: int,
                 headers: dict = {'ContentType': 'application/json'}) -> tuple:
    return json.dumps(content, default=str), status_code, headers


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
        return render_template("/index.html", tasks=Task.get_all())


@routes.route('/tasks', methods=['GET', 'POST'])
def create_task():
    if request.method == 'GET':
        tasks = Task.get_all()
        return JSONResponse({'tasks': [task.to_dict() for task in tasks]}, 200)
    elif request.method == 'POST':
        try:
            task_content = request.form['content']
            new_task = Task(content=task_content).create()
            return JSONResponse({'task': new_task.to_dict()}, 200)
        except NotFound:
            return JSONResponse({'error': 'Task not found'}, 404)
        except Exception as e:
            print(e)
            return JSONResponse({'error': 'Internal Server Error'}, 500)


@routes.route('/tasks/<int:id>', methods=['POST'])
def complete_task(id):
    try:
        task = Task.get(id)
        task.completed = not task.completed
        task.save()
        return JSONResponse({'task': task.to_dict()}, 200)
    except NotFound:
        return JSONResponse({'error': 'Task not found'}, 404)
    except Exception:
        return JSONResponse({'error': 'Internal Server Error'}, 500)


@routes.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    try:
        task = Task.get(id)
        task.content = request.form['content']
        task.save()
        return JSONResponse({'task': task.to_dict()}, 200)
    except NotFound:
        return JSONResponse({'error': 'Task not found'}, 404)
    except Exception:
        return JSONResponse({'error': 'Internal Server Error'}, 500)


@routes.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    try:
        Task.get(id).delete()
        return JSONResponse({}, 204)
    except NotFound:
        return JSONResponse({'error': 'Task not found'}, 404)
    except Exception:
        return JSONResponse({'error': 'Internal Server Error'}, 500)
