from flask import render_template, flash, url_for, redirect, Blueprint, current_app
from flask_login import login_required, current_user, user_logged_in, user_unauthorized
from configparser import ConfigParser
from .. import login_manager, db

parser = ConfigParser()

main = Blueprint('main', __name__)


@main.route("/")
def index():
    print(current_user.get_id())
    return render_template('index.html', cu=(current_user.get_id()))


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Oops! Page Not Found", error=error, cu=current_user.get_id()), 404


