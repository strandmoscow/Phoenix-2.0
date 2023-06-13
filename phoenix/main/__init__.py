from flask import render_template, Blueprint, current_app
from flask_login import current_user
from configparser import ConfigParser

parser = ConfigParser()

main = Blueprint('main', __name__)


@main.route("/")
def index():
    try:
        roles=current_user.get_roles()
    except:
        roles=None
    return render_template('index.html', cu=current_user.get_id(), roles=roles)


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',
                           title="Oops! Page Not Found",
                           error=error,
                           cu=current_user.get_id(),
                           roles=current_user.get_roles()), 404


