from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import psycopg2
import os
from .config_vars import DB_HOST, DB_USER, DB_PASS, DB_NAME

# database handle
try:
    conn = psycopg2.connect(f"dbname='{DB_NAME}' user='{DB_USER}' host='{DB_HOST}' password='{DB_PASS}'")
    cur = conn.cursor()
except:
    print("I am unable to connect to the database")

# encryptor handle
bcrypt = Bcrypt()

# manage user login
login_manager = LoginManager()

UPLOAD_FOLDER = os.path.join('static')


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        UPLOAD_FOLDER=UPLOAD_FOLDER
    )

    with app.app_context():

        # include the routes
        # from eeazycrm import routes
        from phoenix.main import main
        from phoenix.registration.routes import registration
        from phoenix.auth import authentication

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(registration)
        app.register_blueprint(authentication)

        return app
