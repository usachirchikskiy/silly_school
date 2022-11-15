from project.model import db


class Department(db.Model):
    __tablename__ = "department"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))
    name_ru = db.Column(db.String(255))
    name_uz = db.Column(db.String(255))
    description_ru = db.Column(db.Text())
    description_uz = db.Column(db.Text())
    teachers = db.relationship("Teacher", backref="department")