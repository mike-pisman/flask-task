from flask import Blueprint, request
from app.models.task import Task
from app.models.task_list import TaskList
from app.exceptions import NotFound
from app.routes import JSONResponse, login_required_json
from flask_login import current_user

routes = Blueprint("task_list_routes", __name__)


@routes.route("/api/lists", methods=["GET"])
@login_required_json
def get_lists():
    print(current_user.id)
    task_lists = TaskList.get_all(current_user.id)
    return JSONResponse(
        {"lists": [task_list.to_dict() for task_list in task_lists]}, 200
    )


@routes.route("/api/lists", methods=["POST"])
@login_required_json
def create_list():
    try:
        name = request.form["name"]
        account_id = current_user.id
        new_task_list = TaskList(name=name, account_id=account_id).create()
        return JSONResponse({"list": new_task_list.to_dict()}, 201)
    except Exception as e:
        print(e)
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:id>", methods=["PATCH"])
@login_required_json
def update_list(id):
    try:
        task_list = TaskList.get(id)
        task_list.name = request.form["name"]
        task_list.save()
        return JSONResponse({"list": task_list.to_dict()}, 200)
    except NotFound:
        return JSONResponse({"error": "Task list not found"}, 404)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)


@routes.route("/api/lists/<int:id>", methods=["DELETE"])
@login_required_json
def delete_list(id):
    try:
        task_list = TaskList.get(id)
        # Delete all tasks in the list
        for task in task_list.tasks:
            task.delete()
        task_list.delete()
        return JSONResponse({"message": "Task list deleted successfully"}, 200)
    except NotFound:
        return JSONResponse({"error": "Task list not found"}, 404)
    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)