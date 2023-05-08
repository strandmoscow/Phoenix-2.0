from flask import Blueprint, redirect, render_template, session, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from .. import db, auth
from flask_login import login_user, login_required
from ..auth.userLogin import UserLogin
from .models import group as groupdata

groups = Blueprint('groups', __name__, template_folder='templates', static_folder='static')


@groups.route("/group", methods=['GET', 'POST'])
@login_required
def group():

    groups = groupdata.query.all()
    group_student_counts = [(g.group_name, len(g.students)) for g in groups]
    return render_template('groups/groups.html', groups=groups, group_student_counts=group_student_counts)
