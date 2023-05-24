from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField, IntegerField
from wtforms.validators import Email, DataRequired, Regexp


class AccountForm1(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    firstname = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    dob = DateField("Дата рождения", validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])
    passport = StringField("Паспорт", validators=[DataRequired()])

    submit = SubmitField("Продолжить")


class PassportForm(FlaskForm):
    passport_ser = StringField('Серия паспорта', validators=[DataRequired(),
                                                              Regexp(r'/^\d{4}$/',
                                                                     message="Некоректно введена серия")
                                                              ])
    passport_num = StringField('Номер паспорта', validators=[DataRequired(),
                                                              Regexp(r'/^\d{6}$/',
                                                                     message="Некоректно введен номер")
                                                              ])
    passport_podr_code = StringField('Код подразделения')
    passport_podr_name = StringField('Название подразделения', validators=[DataRequired()])