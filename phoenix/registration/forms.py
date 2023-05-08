from flask_wtf import FlaskForm
from wtforms import StringField, DateField, PasswordField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class RegistrationForm1(FlaskForm):
    surname = StringField("Фамилия", validators=[DataRequired()])
    firstname = StringField("Имя", validators=[DataRequired()])
    patronymic = StringField("Отчество")
    email = StringField("Email", validators=[Email(message="Некорректный ввод"), DataRequired()])
    dob = DateField("Дата рождения", validators=[DataRequired()])
    phone = StringField("Номер телефона", validators=[DataRequired()])
    passport = StringField("Паспорт", validators=[DataRequired()])
    submit = SubmitField("Продолжить")


class RegistrationForm2(FlaskForm):
    psw = PasswordField("Пароль: ", validators=[DataRequired(), Length(min=4, max=100,
                                    message="Пароль должен быть от 4 до 100 символов")])
    psw2 = PasswordField("Повтор пароля: ", validators=[DataRequired(), EqualTo(psw, message="Пароли не совпадают")])
    submit = SubmitField("Закончить регистрацию")
