from .. import db


class Attendance(db.Model):
    __tablename__ = 'attendance'

    attendance_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    attendance_lesson_id = db.Column(db.Integer, db.ForeignKey('lesson.lesson_id'), nullable=False)
    attendance_student_id = db.Column(db.Integer, db.ForeignKey('students.student_id'), nullable=False)

    lesson = db.relationship('Lesson', backref='attendances')
    student = db.relationship('Student', backref='attendances')
