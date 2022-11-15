from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

from project.model.Achievement import Achievement
from project.model.Administration import Administration
from project.model.Department import Department
from project.model.Document import Document
from project.model.Gallery import Gallery
from project.model.News import News
from project.model.Teacher import Teacher
from project.model.Faq import Faq
from project.model.SchoolInfo import SchoolInfo
from project.model.Profession import Profession

def init_app(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()
