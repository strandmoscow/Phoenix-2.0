from flask import Blueprint, redirect, render_template, session, request
from flask_login import current_user, user_logged_in
from .forms import RegistrationForm1, RegistrationForm2
from .models import account, val_account
from werkzeug.security import generate_password_hash, check_password_hash
from .. import db

registration = Blueprint('registration', __name__, template_folder='templates')


@registration.route("/regi1", methods=['GET', 'POST'])
def regi1():
    form = RegistrationForm1()
    regi = dict()
    if form.validate_on_submit():
        regi['surname'] = form.surname.data
        regi['fname'] = form.firstname.data
        regi['patronymic'] = form.patronymic.data
        regi['email'] = form.email.data
        regi['DOB'] = form.dob.data
        regi['phone'] = form.phone.data
        session['regi'] = regi
        return redirect("regi2")
    else:
        return render_template('registration/registration.html', form=form, cu=current_user.get_id())


@registration.route("/regi2", methods=['GET', 'POST'])
def regi2():
    form = RegistrationForm2()
    if request.method == 'POST':
        hash = generate_password_hash(form.psw.data)
        session['pwdhash'] = hash
        return redirect("regi3")
    else:
        return render_template('registration/registration2.html', password_dont_match=False,
                               form=form, cu=current_user.get_id())


@registration.route("/regi3", methods=['GET', 'POST'])
def regi3():
    # try:
    a = account(
        account_name=session['regi']['fname'],
        account_surname=session['regi']['surname'],
        account_patronymic=session['regi']['patronymic'],
        account_email=session['regi']['email'],
        account_birthday=session['regi']['DOB'],
        account_phone=session['regi']['phone'],
        account_password=session['pwdhash'],
        account_validated=False
    )
    db.session.add(a)
    db.session.commit()

    aid = db.session.query(account.account_id).filter(account.account_email == session['regi']['email']).first()
    v = val_account(
        account_id=aid[0],
        val_account_name=session['regi']['fname'],
        val_account_surname=session['regi']['surname'],
        val_account_patronymic=session['regi']['patronymic'],
        val_account_email=session['regi']['email'],
        val_account_birthday=session['regi']['DOB'],
        val_account_phone=session['regi']['phone']
    )
    db.session.add(v)
    db.session.commit()

    session.pop('regi')
    # except:
    #     db.session.rollback()
    #     print("Ошибка добавления в БД")

    return render_template('registration/registration3.html', password_dont_match=False, cu=current_user.get_id())
