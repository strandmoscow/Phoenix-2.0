from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Students

from ..registration.models import Account
from ..groups.models import Group
from .. import db, auth

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
@login_required
def student():
    accs = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                            Account.account_patronymic, Students.student_health_insurance,
                            Students.student_birth_certificate, Students.student_snils,
                            Group.group_name, Group.group_id).\
        join(Students, Account.account_student_id == Students.student_id).\
        join(Group, Students.student_group_id == Group.group_id).all()

    # accs = Account.query.filter(Account.account_student_id != None).all()

    return render_template('students/students.html', accs=accs, cu=current_user.get_id())
