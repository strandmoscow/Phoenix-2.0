from flask import Blueprint, redirect, render_template, session, request

trainer = Blueprint('trainer', __name__, template_folder='templates')

