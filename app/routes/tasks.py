from flask import Blueprint, request
from app.models.task import Task
from app.models.task_list import TaskList
from app.exceptions import NotFound
from app.routes import JSONResponse, login_required_json

routes = Blueprint("task_routes", __name__)


@routes.route("/api/lists/<int:list_id>/tasks", methods=["GET"])
@login_required_json
def get_tasks(list_id):
    try:
        # tasks = Task.get_all().filter_by(task_list_id=list_id)
        tasks = TaskList.get(list_id).get_tasks()
        return JSONResponse({"tasks": [task.to_dict() for task in tasks]}, 200)
    except NotFound:
        return JSONResponse({"error": "Task list not found"}, 404)
    except Exception as e:
        print(e)
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:list_id>/tasks", methods=["POST"])
@login_required_json
def create_task(list_id):
    try:
        task_content = request.form["content"]
        task_list = TaskList.get(list_id)
        new_task = Task(content=task_content,
                        task_list_id=task_list.id).create()
        # task_list.add_task(new_task)
        return JSONResponse({"task": new_task.to_dict()}, 201)
    except NotFound:
        return JSONResponse({"error": "Task list not found"}, 404)
    except Exception as e:
        print(e)
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:list_id>/tasks/<int:id>", methods=["POST"])
@login_required_json
def complete_task(list_id, id):
    try:
        task = Task.get(id)
        task.completed = not task.completed
        task.save()
        return JSONResponse({"task": task.to_dict()}, 200)
    except NotFound:
        return JSONResponse({"error": "Task not found"}, 404)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:list_id>/tasks/<int:id>", methods=["PATCH"])
@login_required_json
def update_task(list_id, id):
    try:
        task = Task.get(id)
        task.content = request.form["content"]
        task.save()
        return JSONResponse({"task": task.to_dict()}, 200)
    except NotFound:
        return JSONResponse({"error": "Task not found"}, 404)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:list_id>/tasks/<int:id>", methods=["DELETE"])
@login_required_json
def delete_task(list_id, id):
    try:
        Task.get(id).delete()
        return JSONResponse({}, 204)
    except NotFound:
        return JSONResponse({"error": "Task not found"}, 404)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)
