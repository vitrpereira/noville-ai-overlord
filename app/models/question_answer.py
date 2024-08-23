from models.db import db


class QuestionAnswerModel(db.Model):
    __tablename__ = "question_answers"

    id = db.Column(db.Integer, primary_key=True)
    flag = db.Column(db.String, nullable=False)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
