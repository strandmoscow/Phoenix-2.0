from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, DateField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import Email, DataRequired, Length, EqualTo
from ..account.models import trainer
from ..registration.models import account
from ..students.models import students
from .. import db
from sqlalchemy import not_


class GroupForm1(FlaskForm):
    group_name = StringField("Название группы", validators=[DataRequired()])
    group_trainer = SelectField('Тренер', choices=[], coerce=int)
    group_students = SelectMultipleField('Ученики', choices=[], coerce=int)
    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(GroupForm1, self).__init__(*args, **kwargs)
        trainers = db.session.query(trainer.trainer_id, account.account_name, account.account_patronymic,
                                    account.account_surname).join(account).all()
        self.group_trainer.choices = [
            (t.trainer_id, f"{t.account_name} {t.account_surname}") for
            t in trainers]
        studentsdata = db.session.query(account).filter(account.account_student_id.isnot(None),
                                                    account.students.has(students.student_group_id.is_(None))).all()
        self.group_students.choices = [(student.account_id, f"{student.account_name} {student.account_surname}") for student in studentsdata]
