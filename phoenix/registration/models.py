from .. import db


class account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, unique=True)
    account_name = db.Column(db.String(150))
    account_patronymic = db.Column(db.String(50))
    account_surname = db.Column(db.String(50))
    account_birthday = db.Column(db.Date)
    account_phone = db.Column(db.String(10))
    account_email = db.Column(db.String(150), unique=True)
    account_password = db.Column(db.String)
    account_trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'))
    account_student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    account_parent_id = db.Column(db.Integer, db.ForeignKey('parents.parent_id'))
    account_manager_id = db.Column(db.Integer, db.ForeignKey('manager.manager_id'))
    passport_passport_id = db.Column(db.Integer, db.ForeignKey('passport.passport_id'))
    account_validated = db.Column(db.Boolean)
    students = db.relationship('students', backref='account')

    def __repr__(self):
        return f"Account('{self.account_id}')"


class val_account(db.Model):
    val_account_id = db.Column(db.Integer, primary_key=True, unique=True)
    account_id = db.Column(db.Integer)
    val_account_name = db.Column(db.String(150))
    val_account_patronymic = db.Column(db.String(50))
    val_account_surname = db.Column(db.String(50))
    val_account_birthday = db.Column(db.Date)
    val_account_phone = db.Column(db.String(10))
    val_account_email = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return f"Account('{self.account_id}')"
