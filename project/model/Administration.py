from project.model import db


class Administration(db.Model):
    __tablename__ = "administration"
    id = db.Column(db.Integer, primary_key=True)
    name_ru = db.Column(db.String(255))
    name_uz = db.Column(db.String(255))
    photo = db.Column(db.String(255))
    profession_id = db.Column(db.Integer, db.ForeignKey("profession.id"))