from project.model import db


class Profession(db.Model):
    __tablename__ = "profession"
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(255))
    name_uz = db.Column(db.String(255))
    admins = db.relationship("Administration", backref="profession")