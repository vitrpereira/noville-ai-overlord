from app.models.db import db
from datetime import datetime

class TransactionSplitModel(db.Model):
    __tablename__ = "transactions_splits"

    id = db.Column(db.Integer, primary_key=True)
    transaction_id = db.Column(db.Integer, db.ForeignKey('transactions.id'), nullable=False)
    transaction_date = db.Column(db.Date, nullable=False)
    installment_date = db.Column(db.Date, nullable=False)
    installment_number = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Float, nullable=False)
    amount = db.Column(db.Float, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    transaction = db.relationship('TransactionModel', back_populates='splits')