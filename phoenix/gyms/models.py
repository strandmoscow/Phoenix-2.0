from .. import db


class gym(db.Model):
    gym_id = db.Column(db.Integer, primary_key=True)
    gym_name = db.Column(db.String(64), nullable=False)
    building_building_id = db.Column(db.Integer, db.ForeignKey('building.building_id'), nullable=False)

    building = db.relationship('building', backref='gym')

    def __repr__(self):
        return f'<gym {self.gym_id}>'


class building(db.Model):
    building_id = db.Column(db.Integer, primary_key=True)
    building_name = db.Column(db.String(256), nullable=False)
    building_address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    building_club_id = db.Column(db.Integer, db.ForeignKey('club.club_id'), nullable=False)

    address = db.relationship("address")
    club = db.relationship("club")

    def __repr__(self):
        return f'<building {self.building_id}>'