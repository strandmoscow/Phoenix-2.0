from flask import Flask, send_from_directory, url_for, flash, redirect
from flask_login import LoginManager, current_user
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
import os
from .config_vars import *
from functools import wraps


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
        from phoenix.student.routes import students
        from phoenix.groups.routes import groups
        from phoenix.validation.routes import validation
        from phoenix.trainer.routes import trainer
        from phoenix.clubs.routes import club
        from phoenix.gyms.routes import gym
        from phoenix.attendance.routes import attendance

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
        app.register_blueprint(attendance, url_prefix="/attendance")

        return app


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


def logout_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if current_user.is_authenticated:
            flash("You are already authenticated.", "info")
            return redirect(url_for("main.index"))
        return func(*args, **kwargs)

    return decorated_function
