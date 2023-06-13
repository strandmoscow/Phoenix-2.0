from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import login_user, current_user, user_logged_in, user_unauthorized

from .models import Gym
from .models import Building
from .forms import GymForm1, GymForm2

from ..clubs.models import Address
from ..decoraters import login_required
from .. import db


gym = Blueprint('gym', __name__, template_folder='templates', static_folder='static')


@gym.route("/gyms", methods=['GET', 'POST'])
@login_required
def gyms():

    session = db.session()

    gymstable = session.query(Gym).join(Gym.building).join(Building.address).join(Building.club).join(Address.city).all()

    return render_template('gyms.html', gyms=gymstable, cu=current_user.get_id(), roles=current_user.get_roles())


@gym.route("/gym_add", methods=['GET', 'POST'])
@login_required
def gym_add():
    form = GymForm1()

    if form.validate_on_submit():
        g = Gym(
            gym_name=form.gym_name.data,
            gym_building_id=form.gym_building.data
        )

        db.session.add(g)
        db.session.commit()

        flash('Зал успешно создан', 'success')
        return redirect("gyms")

    return render_template('gym_add.html', form=form, cu=current_user.get_id(), roles=current_user.get_roles())


@gym.route("/gym_edit/<int:gym_id>", methods=['GET', 'POST'])
@login_required
def gym_edit(gym_id):
    gm = Gym.query.get_or_404(gym_id)
    form = GymForm2(obj=Gym.query.get_or_404(gym_id))

    if form.validate_on_submit():
        form.populate_obj(Gym.query.get_or_404(gym_id))
        gm.gym_building_id = form.gym_building.data
        db.session.commit()
        flash('Информация о зале успешно обновлена', 'success')
        return redirect(url_for('gym.gyms', cu=current_user.get_id(), roles=current_user.get_roles()))

    form.gym_building.data = gm.gym_building_id

    return render_template('gym_edit.html', form=form, cu=current_user.get_id(), roles=current_user.get_roles())


@gym.route("/remove_gym/<int:gym_id>", methods=['GET', 'POST'])
@login_required
def remove_gym(gym_id):
    gym_del = Gym.query.get_or_404(gym_id)

    db.session.delete(gym_del)
    db.session.commit()

    flash('Зал успешно удален', 'success')

    return redirect(url_for('gym.gyms', cu=current_user.get_id(), roles=current_user.get_roles()))
