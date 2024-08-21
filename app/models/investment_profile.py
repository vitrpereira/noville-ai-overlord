from models.db import db


class InvestmentProfileModel(db.Model):
    __table__ = "investment_profiles"

    id = db.Column(db.Integer, primary_key=True)
    profile = db.Column(db.String, nullable=False)
    minimum_score = db.Column(db.Integer, nullable=False)
    maximum_score = db.Column(db.Integer, nullable=False)
    metadata = db.Column(db.JSON, nullable=True)
