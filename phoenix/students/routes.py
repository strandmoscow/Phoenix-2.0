from flask import Blueprint, redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from .. import db, auth
from flask_login import login_user, login_required
from ..auth.userLogin import UserLogin

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
def student():
    return render_template('students/students.html')
