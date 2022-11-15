from project.model import db


class Document(db.Model):
    __tablename__ = "document"
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(255))
    name_uz = db.Column(db.String(255))
    file = db.Column(db.String(255))