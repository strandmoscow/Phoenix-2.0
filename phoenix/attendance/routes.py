from flask import Blueprint, redirect, render_template, session, request, flash

from .models import Attendance, Lesson

from .. import db
from ..groups.models import Group
from ..account.models import Trainer
from ..student.models import Students
from ..registration.models import Account

attendance = Blueprint('attendance', __name__, template_folder='templates', static_folder='static')


@attendance.route("/<int:group_id>", methods=['GET', 'POST'])
def att(group_id):

    lessons = Lesson.query.filter_by(lesson_group_id=group_id).all()

    att_by_date = dict()
    for l in lessons:
        att_by_date[l.lesson_datetime] = \
            Attendance.query.filter_by(lesson_group_id=l.lesson_id).all()

    groups = db.session.query(Group.group_name, Account.account_id, Account.account_surname,
                              Account.account_name, db.func.count(Students.student_id), Group.group_id) \
        .join(Trainer, Group.group_trainer_id == Trainer.trainer_id) \
        .join(Account, Trainer.trainer_id == Account.account_trainer_id) \
        .outerjoin(Students, Group.group_id == Students.student_group_id) \
        .group_by(Group.group_name, Account.account_id, Account.account_surname,
                  Account.account_name, Group.group_id) \
        .all()

    print(groups)
    print(att_by_date)

    return render_template("attendance/attendance_of_group.html", group=group_id)
