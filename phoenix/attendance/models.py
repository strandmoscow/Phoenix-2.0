from .. import db


class Lesson(db.Model):
    __tablename__ = 'lesson'

    lesson_id = db.Column(db.Integer, primary_key=True)
    lesson_name = db.Column(db.String(256))
    lesson_datetime = db.Column(db.Date, nullable=False)
    lesson_group_id = db.Column(db.Integer, db.ForeignKey('group.group_id'), nullable=False)
    lesson_gym_id = db.Column(db.Integer, db.ForeignKey('gym.gym_id'), nullable=False)

    group = db.relationship('Group', backref='lessons')
    gym = db.relationship('Gym', backref='lessons')

    def __repr__(self):
        return f"Lesson('{self.lesson_id}')"


class Attendance(db.Model):
    __tablename__ = 'attendance'

    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendance_lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False)
    attendance_student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    lesson = db.relationship('Lesson', backref='attendances')
    student = db.relationship('Students', backref='attendances')

    def __repr__(self):
        return f"Attendance('{self.attendance_id}')"
