from .. import db


class Gym(db.Model):
    gym_id = db.Column(db.Integer, primary_key=True)
    gym_name = db.Column(db.String(64), nullable=False)
    gym_building_id = db.Column(db.Integer, db.ForeignKey('building.building_id'), nullable=False)

    building = db.relationship('Building', backref='gym')

    def __repr__(self):
        return f'<Gym {self.gym_id}>'


class Building(db.Model):
    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(256), nullable=False)
    building_address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    building_club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)

    address = db.relationship("Address")
    club = db.relationship("Club")

    def __repr__(self):
        return f'<Building {self.building_id}>'
