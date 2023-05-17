from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, DateField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import Email, DataRequired, Length, EqualTo
from ..account.models import Trainer
from ..registration.models import Account
from ..student.models import Students
from .models import Address, Federation, Sport
from .. import db
from sqlalchemy import not_


class ClubForm1(FlaskForm):
    club_name = StringField("Название клуба", validators=[DataRequired()])
    club_phone = StringField("Номер клуба", validators=[DataRequired()])
    club_email = StringField("Email клуба", validators=[Email(message="Некорректный ввод"), DataRequired()])
    club_address = SelectField('Адрес', choices=[], coerce=int)
    club_federation = SelectField('Спорт', choices=[], coerce=int)
    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(ClubForm1, self).__init__(*args, **kwargs)
        addresses = db.session.query(Address.address_id, Address.address_street, Address.address_house, Address.address_building).distinct().all()
        self.club_address.choices = [
            (a.address_id, f"{a.address_street}, {a.address_house}, {a.address_building}") for
            a in addresses]
        federations = db.session.query(Federation.federation_id, Sport.sport_name).join(Sport).distinct().all()
        self.club_federation.choices = [(f.federation_id, f"{f.sport_name}") for f in federations]


class ClubForm2(FlaskForm):
    club_name = StringField("Название клуба", validators=[DataRequired()])
    club_phone = StringField("Номер клуба", validators=[DataRequired()])
    club_email = StringField("Email клуба", validators=[Email(message="Некорректный ввод"), DataRequired()])
    club_address = SelectField('Адрес', choices=[], coerce=int)
    club_federation = SelectField('Спорт', choices=[], coerce=int)
    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(ClubForm2, self).__init__(*args, **kwargs)
        addresses = db.session.query(Address.address_id, Address.address_street, Address.address_house,
                                     Address.address_building).distinct().all()
        self.club_address.choices = [
            (a.address_id, f"{a.address_street}, {a.address_house}, {a.address_building}") for
            a in addresses]
        federations = db.session.query(Federation.federation_id, Sport.sport_name).join(Sport).distinct().all()
        self.club_federation.choices = [(f.federation_id, f"{f.sport_name}") for f in federations]
