# This file is part of the Prodeimat project
# @Author: Ricel Quispe

from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os

from .database import db, migrate
from .models import User, Article

# load environment variables from .env file
load_dotenv()


def create_app():
    # initializes flask application
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = (
        f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
        f"@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # initialize SQLAlchemy with this app
    db.init_app(app)
    
    # initialize Flask-Migrate with this app and db
    migrate.init_app(app, db)

    # import all routes
    from .controller.main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .controller.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    from .controller.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')
    
    # manage authentication
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app

