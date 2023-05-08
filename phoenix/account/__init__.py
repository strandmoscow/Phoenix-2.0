from flask import Blueprint, request, render_template, redirect, session
from werkzeug.security import generate_password_hash
import psycopg2
from string import Template



try:
    conn = psycopg2.connect("dbname='Phoenix' user='postgres' host='70.34.250.137' password='p_admin_p'")
    cur = conn.cursor()
    cur.execute("ROLLBACK")
    conn.commit()
except:
    print("I am unable to connect to the database")