from flask import Blueprint, request, flash
from flask_login import login_user, logout_user
from werkzeug.security import check_password_hash
from app.models import Account
from app.routes import JSONResponse, login_required_json

routes = Blueprint('auth_routes', __name__)


@routes.route("/login", methods=['POST'])
def login():
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


@routes.route("/signup", methods=['POST'])
def signup():
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
