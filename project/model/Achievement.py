from project.model import db


class Achievement(db.Model):
    __tablename__ = "achievements"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))