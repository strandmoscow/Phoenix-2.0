from flask import render_template, flash, url_for, redirect, Blueprint, current_app
# from flask_login import login_required
from configparser import ConfigParser

parser = ConfigParser()

main = Blueprint('main', __name__)


@main.route("/")
def index():
    return render_template('index.html')


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', title="Oops! Page Not Found", error=error), 404


@current_app.errorhandler(404)
def page_not_found(error):
    return render_template("404.html", title="Page Not Found")

