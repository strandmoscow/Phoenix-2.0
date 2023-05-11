from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import current_user

from ..registration.models import val_account

validation = Blueprint('validation', __name__, template_folder='templates')


@validation.route("/validation", methods=['GET', 'POST'])
def val():
    val_table = val_account.query.all()

    return render_template("validation/validation.html", cu=current_user.get_id(), val_table=val_table)
