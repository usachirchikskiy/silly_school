
from project.model import db


class SchoolInfo(db.Model):
    __tablename__ = "shool_info"
    id = db.Column(db.Integer, primary_key=True)
    school_number = db.Column(db.Integer)
    telephone_number = db.Column(db.String(255))
    location_name = db.Column(db.String(255))
    location_url = db.Column(db.String(255))
    telegram_url = db.Column(db.String(255))
    instagram_url = db.Column(db.String(255))
    facebook_url = db.Column(db.String(255))
    youtube_url = db.Column(db.String(255))