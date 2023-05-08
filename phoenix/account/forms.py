from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo

class AccountForm1(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    firstname = StringField("Имя", validators=[DataRequired()])
    email = StringField("Email", validators=[Email(), DataRequired()])
    dob = DateField("Дата рождения", validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])
    passport = StringField("Паспорт", validators=[DataRequired()])

    submit = SubmitField("Продолжить")
