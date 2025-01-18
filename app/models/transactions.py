from app.models.db import db
from datetime import datetime

class TransactionModel(db.Model):
    __tablename__ = "transactions"

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    description = db.Column(db.String, nullable=True)
    installments = db.Column(db.Integer, nullable=False)
    payment_method = db.Column(db.String, nullable=False)
    operation = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    splits = db.relationship('TransactionSplitModel', back_populates='transaction')