from models.db import db


class InvestmentProfileModel(db.Model):
    __tablename__ = "investment_profiles"

    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String, nullable=False)
    minimum_score = db.Column(db.Integer, nullable=False)
    maximum_score = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String, nullable=True)
