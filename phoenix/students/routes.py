from flask import Blueprint, redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from .models import students as studentsdata
from .. import db, auth
from flask_login import login_user, login_required, current_user
from ..auth.userLogin import UserLogin

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
@login_required
def student():
    accs = accountdata.query.filter(accountdata.account_student_id != None).all()
    studentstable = studentsdata.query.all()
    return render_template('students/students.html', studentstable=studentstable, accs=accs, cu=current_user.get_id())
