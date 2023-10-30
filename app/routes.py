from flask import Blueprint, render_template, request, redirect, flash, url_for
from . import db
from .models import Todo

routes = Blueprint('routes', __name__)


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


@routes.route("/", methods=['GET', 'POST'])
def home():
    if request.method == 'GET':
        tasks = Todo.query.order_by(Todo.date_created).all()
        import os
        print(os.getcwd())
        return render_template("/index.html", tasks=tasks)
    elif request.method == 'POST':
        print(request)
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except Exception:
            return flash("Something went wrong while adding the task", "danger")


@routes.route('/complete/<int:id>', methods=['POST'])
def complete(id):
    task = Todo.query.get_or_404(id)
    task.completed = not task.completed

    try:
        db.session.commit()
        return redirect('/')
    except Exception:
        return flash("Something went wrong while deleting the task", "danger")


@routes.route('/update/<int:id>', methods=['POST'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except Exception:
            return flash("Something went wrong while deleting the task", "danger")


@routes.route('/delete/<int:id>')
def delete(id):
    task = Todo.query.get_or_404(id)

    try:
        db.session.delete(task)
        db.session.commit()
        return redirect('/')
    except Exception:
        return flash("Something went wrong while deleting the task", "danger")
