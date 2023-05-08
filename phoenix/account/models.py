from .. import db

class passport(db.Model):
    passport_id = db.Column(db.Integer, primary_key=True, unique=True)
    passport_ser = db.Column(db.Integer)
    passport_num = db.Column(db.Integer)
    passport_podr_code = db.Column(db.Integer)
    passport_podr_name = db.Column(db.String(150))

    def __repr__(self):
        return f"Passport('{self.passport_Id}')"
