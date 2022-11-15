from project.model import db

class Faq(db.Model):
    __tablename__ = "faq"
    id = db.Column(db.Integer, primary_key=True)
    question_ru = db.Column(db.Text())
    question_uz = db.Column(db.Text())
    answer_ru = db.Column(db.Text())
    answer_uz = db.Column(db.Text())
