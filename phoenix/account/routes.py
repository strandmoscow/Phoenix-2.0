from flask import Blueprint, redirect, render_template, session, request
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import AccountForm1
from ..registration.models import account as accountdata
from .. import db

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route("/base_acc", methods=['GET', 'POST'])
def base_acc():
    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    acc = accountdata.query.filter_by(account_id=5).first()
    return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc)


@account.route("/acc_edit", methods=['GET', 'POST'])
def acc_edit():
    form = AccountForm1()

    if form.validate_on_submit():
        acc = accountdata.query.filter_by(account_id=5).first()
        acc.account_name = form.firstname.data
        acc.account_surname = form.surname.data
        acc.account_birthday = form.dob.data
        acc.account_phone = form.phone.data
        acc.account_email = form.email.data

        db.session.commit()
        return redirect("base_acc")

    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account/account_edit.html', img=profile_icon, eye=eye_icon, form=form)
