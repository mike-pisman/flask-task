from flask import Blueprint, render_template, request, url_for, redirect
from flask_login import login_required
from app.models.task import Task
from flask_login import current_user


routes = Blueprint("page_routes", __name__)


@routes.route("/", methods=["GET"])
@login_required
def home_page():
    return render_template("index.html", title="home", tasks=Task.get_all())


@routes.route("/login", methods=["GET"])
def login_page():
    if current_user.is_authenticated:
        return redirect(url_for("page_routes.profile_page"))

    return render_template("login.html")


@routes.route("/signup", methods=["GET"])
def signup_page():
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
        tasks["percent"] = round(tasks["done"] / tasks["total"] * 100)
        return render_template("profile.html", tasks=tasks)


@routes.route("/about", methods=["GET"])
def about_page():
    if request.method == "GET":
        return render_template("about.html", title="about")
