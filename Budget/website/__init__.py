from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_login import LoginManager

db_name = "database.db"
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = generate_secret_key()
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{db_name}"
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(auth, url_prefix=("/"))
    app.register_blueprint(views, url_prefix=("/"))

    from .models import User

    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(ID):
        return User.query.get(int(ID))

    with app.app_context():
        db.create_all()
    return app


def generate_secret_key():
    # Check if the SECRET_KEY environment variable is already set
    if "SECRET_KEY" in os.environ:
        return os.environ["SECRET_KEY"]
    else:
        # Generate a random secret key
        return os.urandom(16)
