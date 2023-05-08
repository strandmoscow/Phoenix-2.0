from .. import db


class passport(db.Model):
    passport_id = db.Column(db.Integer, primary_key=True, unique=True)
    passport_ser = db.Column(db.Integer)
    passport_num = db.Column(db.Integer)
    passport_podr_code = db.Column(db.Integer)
    passport_podr_name = db.Column(db.String(150))

    def __repr__(self):
        return f"Passport('{self.passport_id}')"


class parents(db.Model):
    parent_id = db.Column(db.Integer, primary_key=True)
    parent_type_parent_type_id = db.Column(db.Integer, db.ForeignKey('parent_type.parent_type_id'), nullable=False)
    parent_type = db.relationship('parent_type')

    def __repr__(self):
        return f'<parents(parent_id={self.parent_id}, parent_type_parent_type_id={self.parent_type_parent_type_id})>'


class parent_type(db.Model):
    parent_type_id = db.Column(db.Integer, primary_key=True)
    parent_type_name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"parent_type('{self.parent_type_id}')"


class manager(db.Model):
    manager_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"manager('{self.manager_id}')"

class trainer(db.Model):
    trainer_id = db.Column(db.Integer, primary_key=True, unique=True)
    federation_federation_id = db.Column(db.Integer)
    account = db.relationship('account', backref='trainer')

    def __repr__(self):
        return f"trainer'{self.trainer_id}')"