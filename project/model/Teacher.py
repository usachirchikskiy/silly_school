from project.model import db


class Teacher(db.Model):
    __tablename__ = "teacher"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))
    name_ru = db.Column(db.String(255))
    name_uz = db.Column(db.String(255))
    timetable = db.Column(db.String(255))
    department_id = db.Column(db.Integer, db.ForeignKey("department.id"))