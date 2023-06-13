from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import current_user

from .. import db
from ..decoraters import login_required, manager_required
from ..registration.models import Account, ValAccount

validation = Blueprint('validation', __name__, template_folder='templates')


@validation.route("/", methods=['GET', 'POST'])
@manager_required
def val():
    val_table = ValAccount.query.all()

    return render_template("validation.html", cu=current_user.get_id(), roles=current_user.get_roles(), val_table=val_table)


@validation.route("/del/<int:account_id>")
@manager_required
def val_del(account_id):
    ValAccount.query.filter_by(account_id=account_id).delete()

    a = Account.query.filter_by(account_id=account_id).first()
    a.account_validated = True

    db.session.commit()

    return redirect(url_for('validation.val'))


@validation.route("/confirm/<int:account_id>")
@login_required
@manager_required
def val_confirm(account_id):
    val_data = ValAccount.query.filter_by(account_id=account_id).one()

    a = Account.query.filter_by(account_id=account_id).first()

    a.account_name = val_data.val_account_name
    a.account_surname = val_data.val_account_surname
    a.account_patronymic = val_data.val_account_patronymic
    a.account_email = val_data.val_account_email
    a.account_birthday = val_data.val_account_birthday
    a.account_phone = val_data.val_account_phone
    a.account_validated = True

    ValAccount.query.filter_by(account_id=account_id).delete()

    db.session.commit()

    return redirect(url_for('validation.val'))


