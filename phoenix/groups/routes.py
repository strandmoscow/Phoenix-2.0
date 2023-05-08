from flask import Blueprint, redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from .. import db, auth
from flask_login import login_user, login_required, current_user
from ..auth.userLogin import UserLogin
from .models import group as groupdata
from ..account.models import trainer
from ..students.models import students
from sqlalchemy.orm import joinedload

groups = Blueprint('groups', __name__, template_folder='templates', static_folder='static')


@groups.route("/group", methods=['GET', 'POST'])
@login_required
def group():
    # groups = groupdata.query.all()
    # group_student_counts = [(g.group_name, len(g.students)) for g in groups]
    # trs = trainer.query.all()
    # tr = [(t.account.account_surname) for t in trs]
    # return render_template('groups/groups.html', groups=groups, group_student_counts=group_student_counts, cu=current_user.get_id())
    groups = db.session.query(groupdata.group_name, accountdata.account_surname,
                              accountdata.account_name, db.func.count(students.student_id)) \
        .join(trainer, groupdata.group_trainer_id == trainer.trainer_id) \
        .join(accountdata, trainer.trainer_id == accountdata.account_trainer_id) \
        .outerjoin(students, groupdata.group_id == students.student_group_id) \
        .group_by(groupdata.group_name, accountdata.account_surname, accountdata.account_name) \
        .all()

    return render_template('groups/groups.html', groups=groups,
                           cu=current_user.get_id())
