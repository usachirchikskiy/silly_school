import datetime

from project.model import db


class News(db.Model):
    __tablename__ = "news"
    id = db.Column(db.Integer, primary_key=True)
    datetime_posted = db.Column(db.String(255),default=datetime.datetime.now().strftime("%Y-%m-%d %H:%M"))
    name_ru = db.Column(db.String(255))
    description_ru = db.Column(db.Text())
    name_uz = db.Column(db.String(255))
    description_uz = db.Column(db.Text())
    photo = db.Column(db.String(255))