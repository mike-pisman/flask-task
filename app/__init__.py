from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import secrets


# Initialize the app
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

# Database definitions
db = SQLAlchemy()
db.init_app(app)

# Routes
from app.routes import auth, pages, tasks  # noqa: E402
app.register_blueprint(auth.routes)
app.register_blueprint(pages.routes)
app.register_blueprint(tasks.routes)

# Login manager
login_manager = LoginManager()
login_manager.login_view = 'page_routes.login_page'
login_manager.login_message_category = 'danger'
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    from app.models.account import Account
    return Account.query.get(int(user_id))


# Initialize the database
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)
