from project.model import db


class Gallery(db.Model):
    __tablename__ = "gallery"
    id = db.Column(db.Integer, primary_key=True)
    photo = db.Column(db.String(255))