from .. import db


class account(db.Model):
    account_id = db.Column(db.Integer, primary_key=True, unique=True)
    account_name = db.Column(db.String(150))
    account_patronymic = db.Column(db.String(50))
    account_surname = db.Column(db.String(50))
    account_birthday = db.Column(db.Date)
    account_phone = db.Column(db.String(10))
    account_email = db.Column(db.String(150), unique=True)
    account_trainer_id = db.Column(db.Integer)
    # account_student_id = db.Column(db.Integer)
    account_parent_id = db.Column(db.Integer)
    account_manager_id = db.Column(db.Integer)
    passport_passport_id = db.Column(db.Integer)
    account_password = db.Column(db.String)
    account_student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'))
    students = db.relationship('students', backref='account')

    def __repr__(self):
        return f"Account('{self.account_id}')"



