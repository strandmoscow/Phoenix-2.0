from flask import Blueprint, redirect, render_template, session, request, flash, Response, send_file
from flask_login import login_user, current_user
from openpyxl import Workbook
from io import BytesIO

from .models import Students

from ..registration.models import Account
from ..account.models import Manager, Parents, Trainer
from ..groups.models import Group
from .. import db
from ..decoraters import login_required

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
@login_required
def student():
    acc = Account.query.get(current_user.get_id())
    tr = None
    st = None
    pr = None
    mr = None
    if acc:
        if acc.account_trainer_id:
            tr = Trainer.query.get(acc.account_trainer_id)
        elif acc.account_student_id:
            st = Students.query.get(acc.account_student_id)
        elif acc.account_parent_id:
            pr = Parents.query.get(acc.account_parent_id)
        elif acc.account_manager_id:
            mr = Manager.query.get(acc.account_manager_id)
    if tr:
        accs = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                                Account.account_patronymic, Students.student_health_insurance,
                                Students.student_birth_certificate, Students.student_snils,
                                Group.group_name, Group.group_id). \
            join(Students, Account.account_student_id == Students.student_id). \
            join(Group, Students.student_group_id == Group.group_id). \
            filter(Group.group_trainer_id == tr.trainer_id).all()
    elif mr:
        accs = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                                Account.account_patronymic, Students.student_health_insurance,
                                Students.student_birth_certificate, Students.student_snils,
                                Group.group_name, Group.group_id). \
            join(Students, Account.account_student_id == Students.student_id). \
            join(Group, Students.student_group_id == Group.group_id).all()
    else:
        accs = []
    return render_template('students/students.html', accs=accs, cu=current_user.get_id(), trainer=tr, student=st, parent=pr, manager=mr)


@students.route('/export', methods=['GET'])
@login_required
def export_students_table():
    acc = Account.query.get(current_user.get_id())
    tr = None
    st = None
    pr = None
    mr = None
    if acc:
        if acc.account_trainer_id:
            tr = Trainer.query.get(acc.account_trainer_id)
        elif acc.account_student_id:
            st = Students.query.get(acc.account_student_id)
        elif acc.account_parent_id:
            pr = Parents.query.get(acc.account_parent_id)
        elif acc.account_manager_id:
            mr = Manager.query.get(acc.account_manager_id)
    if tr:
        sts_table_data = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                                Account.account_patronymic, Students.student_health_insurance,
                                Students.student_birth_certificate, Students.student_snils,
                                Group.group_name, Group.group_id).\
            join(Students, Account.account_student_id == Students.student_id).\
            join(Group, Students.student_group_id == Group.group_id).\
            filter(Group.group_trainer_id == tr.trainer_id).all()
    elif mr:
        sts_table_data = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                                          Account.account_patronymic, Students.student_health_insurance,
                                          Students.student_birth_certificate, Students.student_snils,
                                          Group.group_name, Group.group_id). \
            join(Students, Account.account_student_id == Students.student_id). \
            join(Group, Students.student_group_id == Group.group_id).all()
    else:
        sts_table_data = []

    # Создаем новый файл Excel и добавляем данные таблицы
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "таблица студентов"

    # Добавляем названия колонок
    column_names = ['ID', 'Фамилия', 'Имя', 'Отчество', 'Медицинская страховка', 'Свидетельство о рождении',
                    'СНИЛС', 'Название группы', 'ID группы']
    worksheet.append(column_names)

    for row in sts_table_data:
        worksheet.append([row.account_id, row.account_surname, row.account_name, row.account_patronymic,
                          row.student_health_insurance, row.student_birth_certificate, row.student_snils,
                          row.group_name, row.group_id])

    # Сохраняем файл в байтовый буфер
    buffer = BytesIO()
    workbook.save(buffer)
    buffer.seek(0)

    # Отправляем файл пользователю для загрузки
    return send_file(buffer, as_attachment=True, download_name='students_data')

