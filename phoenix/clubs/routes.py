from flask import Blueprint, redirect, render_template, flash, url_for
from flask_login import current_user

from .forms import ClubForm1, ClubForm2
from .models import Club
from .models import Federation, Address

from .. import db
from ..decoraters import login_required

club = Blueprint('club', __name__, template_folder='templates', static_folder='static')


@club.route("/templates", methods=['GET', 'POST'])
@login_required
def clubs():
    session = db.session()

    clubstable = session.query(Club).join(Club.address).join(Club.federation).\
        join(Federation.sport).join(Address.city).all()

    return render_template('clubs.html', clubs=clubstable, cu=current_user.get_id(), roles=current_user.get_roles())


@club.route("/club_add", methods=['GET', 'POST'])
@login_required
def club_add():
    form = ClubForm1()

    if form.validate_on_submit():
        c = Club(
            club_name=form.club_name.data,
            club_phone=form.club_phone.data,
            club_email=form.club_email.data,
            club_address_id=form.club_address.data,
            club_federation_id=form.club_federation.data
        )

        db.session.add(c)
        db.session.commit()

        flash('Клуб успешно создан', 'success')
        return redirect("templates")

    return render_template('club_add.html', form=form, cu=current_user.get_id(), roles=current_user.get_roles())


@club.route("/club_edit/<int:club_id>", methods=['GET', 'POST'])
@login_required
def club_edit(club_id):
    cl = Club.query.get_or_404(club_id)
    form = ClubForm2(obj=Club.query.get_or_404(club_id))

    if form.validate_on_submit():
        form.populate_obj(Club.query.get_or_404(club_id))
        cl.club_address_id = form.club_address.data
        cl.club_federation_id = form.club_federation.data
        db.session.commit()
        flash('Информация о клубе успешно обновлена', 'success')
        return redirect(url_for('club.clubs'))

    form.club_address.data = cl.club_address_id
    form.club_federation.data = cl.club_federation_id

    return render_template('club_edit.html', form=form, cu=current_user.get_id(), roles=current_user.get_roles())


@club.route("/remove_club/<int:club_id>", methods=['GET', 'POST'])
@login_required
def remove_club(club_id):
    club_del = Club.query.get_or_404(club_id)

    db.session.delete(club_del)
    db.session.commit()

    flash('Клуб успешно удален', 'success')

    return redirect(url_for('club.clubs'))

