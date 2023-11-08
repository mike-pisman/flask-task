from flask import Blueprint, request
from app.models.task import Task
from app.models.task_list import TaskList
from app.exceptions import NotFound
from app.routes import JSONResponse, login_required_json

routes = Blueprint("task_list_routes", __name__)


@routes.route("/lists", methods=["GET"])
@login_required_json
def get_tasks():
    task_lists = TaskList.get_all()
    return JSONResponse(
        {"lists": [task_list.to_dict() for task_list in task_lists]}, 200
    )


@routes.route("/tasks", methods=["POST"])
@login_required_json
def create_task():
    try:
        list_name = request.form["name"]
        
        new_task_list = TaskList(content=form_content).create()
        return JSONResponse({"task": new_task_list.to_dict()}, 201)

    except Exception:
        return JSONResponse({"error": "Internal Server Error"}, 500)
