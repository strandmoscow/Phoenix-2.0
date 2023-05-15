from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import current_user
from .. import db

from ..registration.models import account, val_account

validation = Blueprint('validation', __name__, template_folder='templates')


@validation.route("/", methods=['GET', 'POST'])
def val():
    val_table = val_account.query.all()

    return render_template("validation/validation.html", cu=current_user.get_id(), val_table=val_table)


@validation.route("/del/<int:account_id>")
def val_del(account_id):
    val_account.query.filter_by(account_id=account_id).delete()
    db.session.commit()

    return redirect(url_for('validation.val'))

@validation.route("/confirm/<int:account_id>")
def val_confirm(account_id):
    val_data = val_account.query.filter_by(account_id=account_id).one()

    a = account.query.filter_by(account_id=account_id).first()

    a.account_name = val_data.val_account_name
    a.account_surname=val_data.val_account_surname
    a.account_patronymic=val_data.val_account_patronymic
    a.account_email=val_data.val_account_email
    a.account_birthday=val_data.val_account_birthday
    a.account_phone=val_data.val_account_phone
    a.account_validated=True

    val_account.query.filter_by(account_id=account_id).delete()

    db.session.commit()


    return redirect(url_for('validation.val'))