from flask import Blueprint, redirect, render_template, session, request
from .forms import RegistrationForm1, RegistrationForm2
from werkzeug.security import generate_password_hash, check_password_hash

registration = Blueprint('registration', __name__, template_folder='templates')
regi = dict()


@registration.route("/regi1", methods=['GET', 'POST'])
def regi1():
    form = RegistrationForm1()
    if form.validate_on_submit():
        regi['surname'] = form.surname.data
        regi['fname'] = form.firstname.data
        regi['email'] = form.email.data
        regi['DOB'] = form.dob.data
        regi['phone'] = form.phone.data
        session['regi'] = regi
        return redirect("regi2")
    else:
        return render_template('registration/registration.html', form=form)


@registration.route("/regi2", methods=['GET', 'POST'])
def regi2():
    form = RegistrationForm2()
    if request.method == 'POST':
        hash = generate_password_hash(form.psw.data)
        session['hashpwd'] = hash
        return redirect("regi3")
    else:
        return render_template('registration/registration2.html', password_dont_match=False, form=form)


@registration.route("/regi3", methods=['GET', 'POST'])
def regi3():
    a = dict()
    a['regi'] = session['regi']
    a['hash'] = session['hash']
    print(a)

    return render_template('registration/registration3.html', password_dont_match=False)