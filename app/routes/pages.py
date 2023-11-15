from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required
from app.models.task import Task
from app.models.task_list import TaskList
from flask_login import current_user


routes = Blueprint("page_routes", __name__)


@routes.route("/", methods=["GET"])
@login_required
def home_page():
    return redirect(url_for("page_routes.lists_page"))


@routes.route("/lists", methods=["GET"])
@login_required
def lists_page():
    lists = TaskList.get_all(current_user.id)
    return render_template("lists.html", title="lists", lists=lists)


@routes.route("/lists/<int:list_id>", methods=["GET"])
@login_required
def list_page(list_id):
    return redirect(url_for("page_routes.task_page", list_id=list_id))


@routes.route("/lists/<int:list_id>/tasks", methods=["GET"])
@login_required
def task_page(list_id):
    task_list = TaskList.get(list_id)
    tasks = task_list.get_tasks()
    return render_template("tasks.html",
                           title="tasks",
                           task_list=task_list,
                           tasks=tasks)


@routes.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("page_routes.profile_page"))

    return render_template("login.html")


@routes.route("/signup", methods=["GET"])
def signup_page():
    if current_user.is_authenticated:
        return redirect(url_for("page_routes.profile_page"))
    return render_template("signup.html")


@routes.route("/profile", methods=["GET"])
@login_required
def profile_page():
    if request.method == "GET":
        all_tasks = Task.get_all()
        tasks = {
            "total": len(all_tasks),
            "done": len([task for task in all_tasks if task.completed]),
            "todo": 0,
            "percent": 0,
        }
        tasks["todo"] = tasks["total"] - tasks["done"]
        if tasks["total"] > 0:
            tasks["percent"] = round(tasks["done"] / tasks["total"] * 100)
        else:
            tasks["percent"] = 0
        return render_template("profile.html", tasks=tasks)


@routes.route("/about", methods=["GET"])
def about_page():
    if request.method == "GET":
        return render_template("about.html", title="about")
