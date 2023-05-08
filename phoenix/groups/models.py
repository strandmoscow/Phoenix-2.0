from .. import db


class group(db.Model):
    group_id = db.Column(db.Integer, primary_key=True, unique=True)
    group_name = db.Column(db.String(150))
    group_trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'))
    trainer = db.relationship('trainer', backref='group')
    students = db.relationship('students', backref='group', lazy=True)

    def __repr__(self):
        return f"group('{self.group_id}')"



