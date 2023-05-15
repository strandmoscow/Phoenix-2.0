from flask import Blueprint, redirect, render_template, session, request, flash

attendance = Blueprint('attendance', __name__, template_folder='templates', static_folder='static')


@attendance.route("/<int:group_id>", methods=['GET', 'POST'])
def att(group):
    return 1


