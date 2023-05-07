from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import generate_password_hash
import psycopg2
from string import Template

registration = Blueprint('registration', __name__, template_folder='templates')
try:
    conn = psycopg2.connect("dbname='Phoenix' user='net_user' host='80.211.80.219' password='net_user_password'")
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
except:
    print("I am unable to connect to the database")


@registration.route("/regi1", methods=['GET', 'POST'])
def regi1():
    if request.method == 'POST':
        regi = dict()
        regi['surname'] = request.form.get('inputSurname')
        regi['fname'] = request.form.get('inputName')
        regi['email'] = request.form.get('inputEmail')
        regi['DOB'] = request.form.get('inputDOB')
        regi['phone'] = request.form.get('inputPhone')
        if request.form.get('inputPhone')[0] == '+':
            regi['phone'] = request.form.get('inputPhone')[1:]
        else:
            regi['phone'] = request.form.get('inputPhone')
        session['regi'] = regi
        return redirect("regi2")
    else:
        return render_template('registration.html')


@registration.route("/regi2", methods=['GET', 'POST'])
def regi2():
    if request.method == 'POST':
        if request.form.get('inputPassword') != request.form.get('confirmPassword'):
            return render_template('registration2.html', password_dont_match=True)
        else:
            pwd = request.form.get('inputPassword')
            hash = generate_password_hash(pwd)
            session['hash'] = hash
            return redirect("regi3")
    else:
        return render_template('registration2.html', password_dont_match=False)


@registration.route("/regi3", methods=['GET', 'POST'])
def regi3():
    a = session['regi']
    a['hash'] = session['hash']
    with open('scenario_registration/sql/regi.sql', 'r') as f:
        src = Template(f.read())
        result = src.substitute(a)
        print(result)
        cur.execute(result)
    return render_template('registration3.html', password_dont_match=False)
