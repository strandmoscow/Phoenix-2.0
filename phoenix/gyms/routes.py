from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.orm import joinedload
from .models import gym as gymdata
from .models import building
from ..clubs.models import address
from .. import db, auth

gym = Blueprint('gym', __name__, template_folder='templates', static_folder='static')

@gym.route("/gyms", methods=['GET', 'POST'])
@login_required
def gyms():

    session = db.session()

    gymstable = session.query(gymdata).join(gymdata.building).join(building.address).join(building.club).join(address.city).all()

    return render_template('gyms/gyms.html', gyms=gymstable, cu=current_user.get_id())
