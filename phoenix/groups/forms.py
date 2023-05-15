from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, DateField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import Email, DataRequired, Length, EqualTo
from ..account.models import Trainer
from ..registration.models import Account
from ..students.models import Students
from .. import db
from sqlalchemy import not_


class GroupForm1(FlaskForm):
    group_name = StringField("Название группы", validators=[DataRequired()])
    group_trainer = SelectField('Тренер', choices=[], coerce=int)
    group_students = SelectMultipleField('Ученики', choices=[], coerce=int)
    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(GroupForm1, self).__init__(*args, **kwargs)
        trainers = db.session.query(Trainer.trainer_id, Account.account_name, Account.account_patronymic,
                                    Account.account_surname).join(Account).all()
        self.group_trainer.choices = [
            (t.trainer_id, f"{t.account_name} {t.account_surname}") for
            t in trainers]
        studentsdata = db.session.query(Account).filter(Account.account_student_id.isnot(None),
                                                    Account.students.has(Students.student_group_id.is_(None))).all()
        self.group_students.choices = [(student.account_id, f"{student.account_name} {student.account_surname}") for student in studentsdata]
