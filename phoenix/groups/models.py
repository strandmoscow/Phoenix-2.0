from .. import db


class Group(db.Model):
    __tablename__ = 'group'

    group_id = db.Column(db.Integer, primary_key=True, unique=True, autoincrement=True)
    group_name = db.Column(db.String(150))
    group_trainer_id = db.Column(db.Integer, db.ForeignKey('trainer.trainer_id'))
    trainer = db.relationship('Trainer', backref='group')
    students = db.relationship('Students', backref='group', lazy=True)

    def __repr__(self):
        return f"group('{self.group_id}')"
