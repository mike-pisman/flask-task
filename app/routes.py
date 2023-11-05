from functools import wraps
import json
from flask import Blueprint, render_template, request, url_for, flash, redirect
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from .models import Task, Account
from .exceptions import NotFound

routes = Blueprint('routes', __name__)


def JSONResponse(content: dict,
                 status_code: int,
                 headers: dict = {'ContentType': 'application/json'}) -> tuple:
    return json.dumps(content, default=str), status_code, headers


def login_required_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not current_user.is_authenticated:
            return JSONResponse({'error': 'Unauthorized'}, 401)
        return f(*args, **kwargs)

    return decorated


@routes.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if current_user.is_authenticated:
            return redirect(url_for('routes.profile_page'))

        return render_template("login.html")
    elif request.method == 'POST':
        try:
            email = request.form['email']
            password = request.form['password']
            remember = request.form['remember'] == "true"
        except KeyError:
            return JSONResponse({'error': 'Invalid request body'}, 400)

        user = Account.query.filter_by(email=email).first()

        # Check if the user actually exists
        # Hash the password and compare it to the stored one in the database
        if not user or not check_password_hash(user.password, password):
            return JSONResponse(
                {'error': 'Please check your login details and try again.'},
                401)

        # Log in the user
        login_user(user, remember=remember)

        # Return a response to the user
        flash('Logged in successfully', 'success')
        return JSONResponse({'message': 'Logged in successfully'}, 200)


@routes.route("/logout", methods=['POST'])
@login_required_json
def logout():
    if request.method == 'POST':
        logout_user()
        flash('Logged out successfully', 'success')
        return JSONResponse({'message': 'Logged out successfully'}, 200)


@routes.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
        # Get the form data
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        # Check if account already exists
        account = Account.query.filter_by(email=email).first()
        if account:
            return JSONResponse(
                {'error': 'Account with such email already exists'}, 400)

        # Create a new user with the form data.
        Account(email, name, password).create()

        # Return a response to the user
        flash('Account created successfully', 'success')
        return JSONResponse({'message': 'Account created successfully'}, 201)


@routes.route("/", methods=['GET'])
@login_required
def home():
    if request.method == 'GET':
        return render_template("index.html", title="home", tasks=Task.get_all())


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


@routes.route('/profile', methods=['GET'])
@login_required
def profile_page():
    if request.method == 'GET':
        all_tasks = Task.get_all()
        tasks = {
            'total': len(all_tasks),
            'done': len([task for task in all_tasks if task.completed]),
            'todo': 0,
            'percent': 0
        }
        tasks['todo'] = tasks['total'] - tasks['done']
        tasks['percent'] = round(tasks['done'] / tasks['total'] * 100)
        return render_template("profile.html", tasks=tasks)


@routes.route('/about', methods=['GET'])
def about_page():
    if request.method == 'GET':
        return render_template("about.html", title="about")
