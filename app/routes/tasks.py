from flask import Blueprint, request
from app.models import Task
from app.exceptions import NotFound
from app.routes import JSONResponse, login_required_json

routes = Blueprint('task_routes', __name__)


@routes.route("/tasks", methods=['GET'])
@login_required_json
def get_tasks():
    if request.method == 'GET':
        tasks = Task.get_all()
        return JSONResponse({'tasks': [task.to_dict() for task in tasks]}, 200)


@routes.route('/tasks', methods=['POST'])
@login_required_json
def create_task():
    if request.method == 'POST':
        try:
            task_content = request.form['content']
            new_task = Task(content=task_content).create()
            return JSONResponse({'task': new_task.to_dict()}, 201)
        except NotFound:
            return JSONResponse({'error': 'Task not found'}, 404)
        except Exception:
            return JSONResponse({'error': 'Internal Server Error'}, 500)


@routes.route('/tasks/<int:id>', methods=['POST'])
@login_required_json
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
@login_required_json
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
@login_required_json
def delete_task(id):
    try:
        Task.get(id).delete()
        return JSONResponse({}, 204)
    except NotFound:
        return JSONResponse({'error': 'Task not found'}, 404)
    except Exception:
        return JSONResponse({'error': 'Internal Server Error'}, 500)
