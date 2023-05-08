from flask import Blueprint, redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from .models import students as studentsdata
from ..groups.models import group as groupdata
from .. import db, auth
from flask_login import login_user, login_required, current_user

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
@login_required
def student():
    accs = db.session.query(accountdata.account_surname, accountdata.account_name, accountdata.account_patronymic, studentsdata.student_health_insurance, studentsdata.student_birth_certificate, studentsdata.student_snils, groupdata.group_name).\
        join(studentsdata, accountdata.account_student_id == studentsdata.student_id).\
        join(groupdata, studentsdata.student_group_id == groupdata.group_id).all()

    # accs = accountdata.query.filter(accountdata.account_student_id != None).all()

    return render_template('students/students.html', accs=accs, cu=current_user.get_id())
