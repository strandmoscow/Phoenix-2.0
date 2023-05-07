from flask import Blueprint, redirect, render_template, session, request
from werkzeug.security import generate_password_hash, check_password_hash

account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route("/base_acc", methods=['GET', 'POST'])
def base_acc():
    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account/account.html', img=profile_icon, eye=eye_icon)


@account.route("/acc_edit", methods=['GET', 'POST'])
def acc_edit():
    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account/account_edit.html', img=profile_icon, eye=eye_icon)
