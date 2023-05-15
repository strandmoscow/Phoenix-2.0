from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import login_user, login_required, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import AccountForm1
from ..registration.models import account as accountdata
from ..registration.models import val_account as val_accountdata
from .models import passport, parents, manager, trainer
from ..students.models import students
from .. import db, auth


account = Blueprint('account', __name__, template_folder='templates', static_folder='static')

@account.route("/edit", methods=['GET', 'POST'])
@login_required
def acc_edit():
    acc = accountdata.query.get(current_user.get_id())
    form = AccountForm1()

    if form.validate_on_submit():
        acc = accountdata.query.filter_by(account_id=current_user.get_id()).first()
        v = val_accountdata(
            account_id=int(current_user.get_id()),
            val_account_name=form.firstname.data,
            val_account_surname=form.surname.data,
            val_account_patronymic=form.patronymic.data,
            val_account_email=form.email.data,
            val_account_birthday=form.dob.data,
            val_account_phone=form.phone.data
        )
        db.session.add(v)

        acc.account_validated = False

        db.session.commit()
        flash('Your data is on validation', 'success')
        return redirect(url_for('account.accountfull', account_id=current_user.get_id()))

    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account/account_edit.html', img=profile_icon, eye=eye_icon, form=form,
                           cu=current_user.get_id(), acc=acc)


@account.route('/<int:account_id>')
def accountfull(account_id):
    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    acc = accountdata.query.get(account_id)
    if acc:
        if acc.account_trainer_id:
            tr = trainer.query.get(acc.account_trainer_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, trainer=tr, cu=int(current_user.get_id()))
        elif acc.account_student_id:
            st = students.query.get(acc.account_student_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, student=st, cu=int(current_user.get_id()))
        elif acc.account_parent_id:
            pr = parents.query.get(acc.account_parent_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, parent=pr, cu=int(current_user.get_id()))
        elif acc.account_manager_id:
            mr = manager.query.get(acc.account_manager_id)
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, manager=mr, cu=int(current_user.get_id()))
        else:
            return render_template('account/account.html', img=profile_icon, eye=eye_icon, acc=acc, cu=int(current_user.get_id()))
    return "Account not found", 404