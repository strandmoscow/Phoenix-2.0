from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from .models import Gym
from .models import Building
from ..clubs.models import Address
from .. import db, auth

gym = Blueprint('gym', __name__, template_folder='templates', static_folder='static')

@gym.route("/gyms", methods=['GET', 'POST'])
@login_required
def gyms():

    session = db.session()

    gymstable = session.query(Gym).join(Gym.building).join(Building.address).join(Building.club).join(Address.city).all()

    return render_template('gyms/gyms.html', gyms=gymstable, cu=current_user.get_id())
