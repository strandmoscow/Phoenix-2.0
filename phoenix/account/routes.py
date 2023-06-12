from flask import Blueprint, redirect, render_template, session, request, flash, url_for
from flask_login import login_user, current_user, user_logged_in, user_unauthorized
from werkzeug.security import generate_password_hash, check_password_hash

from .forms import AccountForm1, PassportForm
from .models import Parents, Manager, Trainer, Passport

from ..registration.models import Account
from ..registration.models import ValAccount
from ..student.models import Students
from ..decoraters import login_required, manager_required
from .. import db


account = Blueprint('account', __name__, template_folder='templates', static_folder='static')


@account.route("/edit", methods=['GET', 'POST'])
@login_required
def acc_edit():
    acc = Account.query.filter_by(account_id=current_user.get_id()).first()
    form = AccountForm1()

    if form.validate_on_submit():
        v = ValAccount(
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
    else:
        form.firstname.data = acc.account_name
        form.surname.data = acc.account_surname
        form.patronymic.data = acc.account_patronymic
        form.email.data = acc.account_email
        form.dob.data = acc.account_birthday
        form.phone.data = acc.account_phone

    profile_icon = './static/svg/abstract-user-flat-4.svg'
    eye_icon = './static/svg/eye.svg'
    return render_template('account_edit.html', img=profile_icon, eye=eye_icon, form=form,
                           cu=current_user.get_id(), acc=acc)


@account.route('/<int:account_id>')
@login_required
def accountfull(account_id):
    acc = Account.query.get(account_id)
    if acc:
        if acc.account_trainer_id:
            tr = Trainer.query.get(acc.account_trainer_id)
            return render_template('account.html', acc=acc, trainer=tr, cu=int(current_user.get_id()))
        elif acc.account_student_id:
            st = Students.query.get(acc.account_student_id)
            return render_template('account.html', acc=acc, student=st, cu=int(current_user.get_id()))
        elif acc.account_parent_id:
            pr = Parents.query.get(acc.account_parent_id)
            return render_template('account.html', acc=acc, parent=pr, cu=int(current_user.get_id()))
        elif acc.account_manager_id:
            mr = Manager.query.get(acc.account_manager_id)
            return render_template('account.html', acc=acc, manager=mr, cu=int(current_user.get_id()))
        else:
            return render_template('account.html', acc=acc, cu=int(current_user.get_id()))
    return "Account not found", 404


@account.route('/<int:account_id>/docs')
@login_required
def documents(account_id):
    acc = Account.query.get(account_id)
    passport_data = Passport.query.filter_by(passport_id=acc.account_passport_id).first()
    if acc:
        if passport_data:
            return render_template('documents.html',
                                   acc=acc,
                                   cu=current_user.get_id(),
                                   pas=passport_data)
        else:
            return render_template('documents.html',
                                   acc=acc,
                                   cu=current_user.get_id(),
                                   pas=False)
    return "Account not found", 404


@account.route('/<int:account_id>/docs/pasadd', methods=['GET', 'POST'])
@login_required
def passadd(account_id):
    form = PassportForm()
    acc = Account.query.get(account_id)

    if form.validate_on_submit():
        p = Passport(
            passport_ser=form.passport_ser.data,
            passport_num=form.passport_num.data,
            passport_podr_code=form.passport_podr_code.data,
            passport_podr_name=form.passport_podr_name.data
        )

        db.session.add(p)
        db.session.flush()
        db.session.refresh(p)

        acc.account_passport_id = p.passport_id
        db.session.commit()
        return redirect(url_for('account.documents', account_id=acc.account_id))

    return render_template('passport_add.html', form=form, acc=acc, cu=current_user.get_id())