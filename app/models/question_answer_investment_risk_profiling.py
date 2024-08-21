from models.db import db

class QuestionAsnwerInvestmentRiskProfilingModel(db.Model):
    __tablename__ = "question_answers_investment_risk_profiling"

    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String, nullable=False)
    answer = db.Column(db.String, nullable=False)
    score = db.Column(db.Integer, nullable=False)
    profile_id = db.Column(db.Integer, db.ForeignKey('investment_profiles.id'), nullable=False)
    profile = db.relationship('InvestmentProfileModel', backref=db.backref('questions_answers', lazy=True))
