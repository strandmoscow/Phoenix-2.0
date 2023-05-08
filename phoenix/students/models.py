from .. import db


class students(db.Model):
    student_id = db.Column(db.Integer, primary_key=True, unique=True)
    student_health_insurance = db.Column(db.Integer)
    student_birth_certificate = db.Column(db.Integer)
    student_snils = db.Column(db.Integer)
    student_group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'))

    def __repr__(self):
        return f"Students('{self.student_Id}')"
