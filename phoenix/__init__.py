from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from .config_vars import *


# app initialisation
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY=SECRET_KEY
    )

# app initialisation
app = Flask(__name__, instance_relative_config=True)
app.config.from_mapping(
        SECRET_KEY='dev'
    )

# database handle
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
db = SQLAlchemy(app)

# encryptor handle
bcrypt = Bcrypt()

# manage user login
login_manager = LoginManager(app)

UPLOAD_FOLDER = os.path.join('static')


def create_app():
    with app.app_context():
        # include the routes
        # from phoenix import routes
        from phoenix.main import main
        from phoenix.registration.routes import registration
        from phoenix.auth.routes import authentication
        from phoenix.account.routes import account
        from phoenix.students.routes import students
        from phoenix.groups.routes import groups
        from phoenix.validation.routes import validation
        from phoenix.trainer.routes import trainer
        from phoenix.clubs.routes import club
        from phoenix.gyms.routes import gym

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(registration, url_prefix="/reg")
        app.register_blueprint(authentication, url_prefix="/auth")
        app.register_blueprint(account, url_prefix="/account")
        app.register_blueprint(students, url_prefix="/students")
        app.register_blueprint(groups, url_prefix="/group")
        app.register_blueprint(validation, url_prefix="/val")
        app.register_blueprint(trainer, url_prefix="/trainer")
        app.register_blueprint(club, url_prefix="/club")
        app.register_blueprint(gym, url_prefix="/gym")

        return app
