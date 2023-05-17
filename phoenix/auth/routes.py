from flask import Blueprint, redirect, render_template, session, request, url_for, flash
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, current_user, user_logged_in
from .. import db, login_manager, logout_required

from .userLogin import UserLogin
from .forms import Login
from .models import Account

authentication = Blueprint('auth', __name__, template_folder='templates')


@login_manager.user_loader
def load_user(user_id):
    print("load_user")
    return UserLogin().fromDB(user_id, db)


@authentication.route("/", methods=['GET', 'POST'])
@logout_required
def auth():
    form = Login()
    if form.validate_on_submit():
        user = Account.query.filter_by(account_email=form.email.data).first()
        if user and check_password_hash(user.account_password, form.password.data):
            userLogin = UserLogin().create(user)
            if form.remember.data:
                login_user(userLogin, remember=True)
            else:
                login_user(userLogin)
            return redirect(url_for('main.index'))
        else:
            print("Some problems")
            return render_template('auth/auth.html', form=form, logging_in_err=True, cu=current_user.get_id(), loginer=True)

    return render_template('auth/auth.html', form=form, logging_in_err=False, cu=current_user.get_id())


@authentication.route("/exit")
def exit():
    logout_user()
    if session.get('was_once_logged_in'):
        # prevent flashing automatically logged out message
        del session['was_once_logged_in']
    flash('You have successfully logged yourself out.')
    return redirect(url_for('main.index'))


