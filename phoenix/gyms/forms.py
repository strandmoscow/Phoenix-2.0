from flask_wtf import FlaskForm
from sqlalchemy.orm import joinedload
from wtforms import StringField, DateField, PasswordField, SubmitField, SelectField, SelectMultipleField
from wtforms.validators import Email, DataRequired, Length, EqualTo
from ..account.models import Trainer
from ..registration.models import Account
from ..student.models import Students
from .models import Gym, Building
from ..clubs.models import Address
from .. import db
from sqlalchemy import not_


class GymForm1(FlaskForm):
    gym_name = StringField("Название зала", validators=[DataRequired()])
    gym_building = SelectField('Здание', choices=[], coerce=int)

    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(GymForm1, self).__init__(*args, **kwargs)
        buildings = db.session.query(Building.building_id, Building.building_name, Address.address_street,
                                     Address.address_building, Address.address_house). \
            join(Gym, Gym.gym_building_id == Building.building_id). \
            join(Address, Building.building_address_id == Address.address_id). \
            distinct(Building.building_id).all()
        self.gym_building.choices = [
            (b.building_id, f"{b.building_name}, адрес: {b.address_street} {b.address_house}, {b.address_building} ") for b in
            buildings]


class GymForm2(FlaskForm):
    gym_name = StringField("Название зала", validators=[DataRequired()])
    gym_building = SelectField('Здание', choices=[], coerce=int)

    submit = SubmitField("Продолжить")

    def __init__(self, *args, **kwargs):
        super(GymForm2, self).__init__(*args, **kwargs)
        buildings = db.session.query(Building.building_id, Building.building_name, Address.address_street,
                                     Address.address_building, Address.address_house). \
            join(Gym, Gym.gym_building_id == Building.building_id). \
            join(Address, Building.building_address_id == Address.address_id). \
            distinct(Building.building_id).all()
        self.gym_building.choices = [
            (b.building_id, f"{b.building_name}, адрес: {b.address_street} {b.address_house}, {b.address_building} ") for b in
            buildings]
