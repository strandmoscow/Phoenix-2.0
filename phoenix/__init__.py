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
        from phoenix.validation.routes import validation

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(registration)
        app.register_blueprint(authentication)
        app.register_blueprint(account)
        app.register_blueprint(students)
        app.register_blueprint(validation)

        return app
