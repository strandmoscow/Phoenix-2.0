from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, TimeField, FieldList, BooleanField
from wtforms.validators import DataRequired
from datetime import datetime


class AttendanceForm(FlaskForm):
    date = DateField("Дата занятия",
                     validators=[DataRequired()],
                     format='%Y-%m-%d',
                     default=datetime.now())
    time = TimeField('Time',
                     format='%H:%M',
                     default=datetime.now())
    gym = SelectField("Зал")
    attendance = FieldList(BooleanField(), min_entries=1, label="Посещения")
