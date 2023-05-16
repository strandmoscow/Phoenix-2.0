from .. import db


class Club(db.Model):
    club_id = db.Column(db.Integer, primary_key=True)
    club_name = db.Column(db.String(256), nullable=False)
    club_phone = db.Column(db.String(256), nullable=False)
    club_email = db.Column(db.String(256), nullable=False)
    club_address_id = db.Column(db.Integer, db.ForeignKey('address.address_id'), nullable=False)
    club_federation_id = db.Column(db.Integer, db.ForeignKey('federation.federation_id'), nullable=False)

    address = db.relationship('Address')
    federation = db.relationship('Federation')

    def __repr__(self):
        return f"<club {self.club_id}>"


class Federation(db.Model):
    federation_id = db.Column(db.Integer, primary_key=True)
    federation_sport = db.Column(db.Integer, db.ForeignKey('sport.sport_id'), nullable=False)

    sport = db.relationship('Sport')

    def __repr__(self):
        return f"<federation {self.federation_id}>"


class Sport(db.Model):
    sport_id = db.Column(db.Integer, primary_key=True)
    sport_name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<sport {self.sport_id}>"


class Address(db.Model):
    address_id = db.Column(db.Integer, primary_key=True)
    address_country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    address_region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    address_city_id = db.Column(db.Integer, db.ForeignKey('city.city_id'), nullable=False)
    address_street = db.Column(db.String(64), nullable=False)
    address_house = db.Column(db.Integer, nullable=False)
    address_building = db.Column(db.String(64), nullable=False)

    city = db.relationship('City')

    def __repr__(self):
        return f'<аddress {self.address_id}>'


class Country(db.Model):
    country_id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f'<country {self.country_id}>'


class Region(db.Model):

    region_id = db.Column(db.Integer, primary_key=True)
    region_name = db.Column(db.String(256), nullable=False)
    region_country_id = db.Column(db.Integer, db.ForeignKey('country.country_id'), nullable=False)
    country = db.relationship('Country', backref=db.backref('region', lazy=True))

    def __repr__(self):
        return f'<region {self.region_id}>'


class City(db.Model):
    city_id = db.Column(db.Integer, primary_key=True)
    city_name = db.Column(db.String(256), nullable=False)
    city_region_id = db.Column(db.Integer, db.ForeignKey('region.region_id'), nullable=False)
    region = db.relationship('Region', backref='city')

    def __repr__(self):
        return f'<city {self.city_id}>'
