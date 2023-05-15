from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from ..registration.models import Account
from ..students.models import Students
from sqlalchemy.orm import joinedload
from .. import db, auth
from .models import club as clubdata
from .models import federation, city, address

club = Blueprint('club', __name__, template_folder='templates', static_folder='static')


@club.route("/clubs", methods=['GET', 'POST'])
@login_required
def clubs():
    session = db.session()

    clubstable = session.query(clubdata).join(clubdata.address).join(clubdata.federation).join(federation.sport).join(address.city).all()

    return render_template('clubs/clubs.html', clubs=clubstable, cu=current_user.get_id())


