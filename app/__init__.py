from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import secrets



# Initialize the app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SECRET_KEY'] = secrets.token_urlsafe(16)

# Database definitions
db = SQLAlchemy()
db.init_app(app)

# Initialize the database
with app.app_context():
    db.create_all()

# Routes
from . import routes
app.register_blueprint(routes.routes)

if __name__ == "__main__":
    app.run(debug=True)
