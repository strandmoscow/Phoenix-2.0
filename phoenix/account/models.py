from .. import db


class Passport(db.Model):
    __tablename__ = 'passport'

    passport_id = db.Column(db.Integer, primary_key=True, unique=True)
    passport_ser = db.Column(db.Integer)
    passport_num = db.Column(db.Integer)
    passport_podr_code = db.Column(db.Integer)
    passport_podr_name = db.Column(db.String(150))

    def __repr__(self):
        return f"Passport('{self.passport_id}')"


class Parents(db.Model):
    __tablename__ = 'parents'

    parent_id = db.Column(db.Integer, primary_key=True)
    parent_type_parent_type_id = db.Column(db.Integer, db.ForeignKey('parent_type.parent_type_id'), nullable=False)
    parent_type = db.relationship('ParentType')

    def __repr__(self):
        return f'<parents(parent_id={self.parent_id}, parent_type_parent_type_id={self.parent_type_parent_type_id})>'


class ParentType(db.Model):
    __tablename__ = 'parent_type'

    parent_type_id = db.Column(db.Integer, primary_key=True)
    parent_type_name = db.Column(db.String(256), nullable=False)

    def __repr__(self):
        return f"parent_type('{self.parent_type_id}')"


class Manager(db.Model):
    __tablename__ = 'manager'

    manager_id = db.Column(db.Integer, primary_key=True)

    def __repr__(self):
        return f"manager('{self.manager_id}')"


class Trainer(db.Model):
    __tablename__ = 'trainer'

    trainer_id = db.Column(db.Integer, primary_key=True, unique=True)
    federation_federation_id = db.Column(db.Integer)
    account = db.relationship('Account', backref='trainer')

    def __repr__(self):
        return f"trainer'{self.trainer_id}')"
