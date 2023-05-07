from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
import psycopg2
import os

# database handle
try:
    conn = psycopg2.connect("dbname='Phoenix' user='postgres' host='70.34.250.137' password='p_admin_p'")
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

    with app.app_context():

        # include the routes
        # from eeazycrm import routes
        from main import main
        from registration import registration
        from auth import authentication

        # register routes with blueprint
        app.register_blueprint(main)
        app.register_blueprint(registration)
        app.register_blueprint(authentication)

        return app