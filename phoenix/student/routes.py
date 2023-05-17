from flask import Blueprint, redirect, render_template, session, request, flash, Response, send_file
from flask_login import login_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from .models import Students

from ..registration.models import Account
from ..groups.models import Group
from .. import db, auth
from openpyxl import Workbook
from io import BytesIO

students = Blueprint('students', __name__, template_folder='templates', static_folder='static')


@students.route("/student", methods=['GET', 'POST'])
@login_required
def student():
    accs = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                            Account.account_patronymic, Students.student_health_insurance,
                            Students.student_birth_certificate, Students.student_snils,
                            Group.group_name, Group.group_id).\
        join(Students, Account.account_student_id == Students.student_id).\
        join(Group, Students.student_group_id == Group.group_id).all()

    # accs = Account.query.filter(Account.account_student_id != None).all()

    return render_template('students/students.html', accs=accs, cu=current_user.get_id())


@students.route('/export', methods=['GET'])
def export_students_table():
    sts_table_data = db.session.query(Account.account_id, Account.account_surname, Account.account_name,
                            Account.account_patronymic, Students.student_health_insurance,
                            Students.student_birth_certificate, Students.student_snils,
                            Group.group_name, Group.group_id).\
        join(Students, Account.account_student_id == Students.student_id).\
        join(Group, Students.student_group_id == Group.group_id).all()

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

