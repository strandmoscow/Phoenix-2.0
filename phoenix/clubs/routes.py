from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import account as accountdata
from ..students.models import students
from .. import db, auth

club = Blueprint('club', __name__, template_folder='templates', static_folder='static')

@club.route("/clubs", methods=['GET', 'POST'])
@login_required
def clubs():


    return render_template('clubs/clubs.html', cu=current_user.get_id())


