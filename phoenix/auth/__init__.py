from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import generate_password_hash
import psycopg2
from string import Template

authentication = Blueprint('auth', __name__, template_folder='templates')
try:
    conn = psycopg2.connect("dbname='Phoenix' user='postgres' host='70.34.250.137' password='p_admin_p'")
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
except:
    print("I am unable to connect to the database")


@authentication.route("/a", methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        a = dict()
        a['email'] = request.form.get('inputEmail1')
        pwd = request.form.get('inputPassword1')
        with open('scenario_auth/sql/get_pwd.sql', 'r') as f:
            src = Template(f.read())
            result = src.substitute(a)
            print(result)
            cur.execute(result)
        return render_template('index.html')
    else:
        return render_template('auth.html')

