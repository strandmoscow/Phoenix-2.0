from flask import Blueprint, redirect, render_template, session, request, flash
from flask_login import login_user, login_required, current_user
from collections import namedtuple

from .models import Attendance, Lesson
from .forms import AttendanceForm

from .. import db
from ..groups.models import Group
from ..student.models import Students
from ..registration.models import Account
from ..gyms.models import Gym

attendance = Blueprint('attendance', __name__, template_folder='templates', static_folder='static')


@attendance.route("/<int:group_id>", methods=['GET', 'POST'])
def att(group_id):
    group = Group.query.get(group_id)

    lessons = Lesson.query.filter_by(lesson_group_id=group_id).all()

    att_by_date = dict()
    for l in lessons:
        att_by_date[l.lesson_datetime] = \
            Attendance.query.filter_by(attendance_lesson_id=l.lesson_id).all()

    sts = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                           Account.account_patronymic). \
        join(Students, Account.account_student_id == Students.student_id). \
        join(Group, Students.student_group_id == Group.group_id) \
        .filter(Group.group_id == group_id) \
        .all()

    att_to_func = dict()

    for p in sts:
        if p[3]:
            key = str(p[0]) + ":" + p[1] + ' ' + p[2] + ' ' + p[3]
        else:
            key = str(p[0]) + ":" + p[1] + ' ' + p[2]
        att_to_func[key] = []
        for date in att_by_date.keys():
            flag = True
            for a in att_by_date[date]:
                flag = True
                if p[0] == a.attendance_student_id:
                    att_to_func[key].append(True)
                    flag = False
            if flag:
                att_to_func[key].append(False)

    return render_template("attendance/attendance_of_group.html",
                           group=group,
                           dates=att_by_date.keys(),
                           att_to_func=att_to_func,
                           cu=current_user.get_id())


@attendance.route('/<int:group_id>/new', methods=['GET', 'POST'])
def att_new(group_id):
    group = Group.query.get(group_id)

    sts = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                           Account.account_patronymic). \
        join(Students, Account.account_student_id == Students.student_id). \
        join(Group, Students.student_group_id == Group.group_id) \
        .filter(Group.group_id == group_id) \
        .all()

    att_list = []
    AttOfPerson = namedtuple('AttOfPerson', ['ID', 'ФИО'])
    for p in sts:
        if p[3]:
            att_list.append(AttOfPerson(p[0], p[1] + ' ' + p[2] + ' ' + p[3]))
        else:
            att_list.append(AttOfPerson(p[0], p[1] + ' ' + p[2]))

    data = {'att': att_list}
    print(data)

    GymT = namedtuple('GymT', ['ID', 'Name'])
    gym_list = []

    gyms = Gym.query.all()
    for g in gyms:
        gym_list.append(GymT(g.gym_id, g.gym_name))

    form = AttendanceForm(data=data)
    form.gym.choices = gym_list

    return render_template("attendance/attendance_new.html",
                           group=group,
                           cu=current_user.get_id(),
                           form=form)
