from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import AccountForm1
from ..registration.models import account as accountdata
from .models import passport, parents, manager, trainer
from ..students.models import students
from .. import db, auth


account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


# @account.route("/base_acc", methods=['GET', 'POST'])
# @login_required
# def base_acc():
#     profile_icon = './static/svg/abstract-user-flat-4.svg'
#     eye_icon = './static/svg/eye.svg'
#     acc = accountdata.query.filter_by(account_id=current_user.get_id()).first()
#     return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, cu=user_logged_in)


@account.route("/acc_edit", methods=['GET', 'POST'])
@login_required
def acc_edit():

    form = AccountForm1()

    if form.validate_on_submit():
        acc = accountdata.query.filter_by(account_id=current_user.get_id()).first()
        acc.account_name = form.firstname.data
        acc.account_surname = form.surname.data
        acc.account_birthday = form.dob.data
        acc.account_phone = form.phone.data
        acc.account_email = form.email.data

        db.session.commit()
        flash('The account has been successfully updated', 'success')
        return redirect("base_acc")

    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account/account_edit.html', img=profile_icon, eye=eye_icon, form=form,
                           cu=current_user.get_id())

@account.route('/account/<int:account_id>')
def accountfull(account_id):
    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    acc = accountdata.query.get(account_id)
    if acc:
        if acc.account_trainer_id:
            tr = trainer.query.get(acc.account_trainer_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, trainer=tr, cu=current_user.get_id())
        elif acc.account_student_id:
            st = students.query.get(acc.account_student_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, student=st, cu=current_user.get_id())
        elif acc.account_parent_id:
            pr = parents.query.get(acc.account_parent_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, parent=pr, cu=current_user.get_id())
        elif acc.account_manager_id:
            mr = manager.query.get(acc.account_manager_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, manager=mr, cu=current_user.get_id())
        else:
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, cu=current_user.get_id())
    return "Account not found", 404