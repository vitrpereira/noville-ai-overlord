import csv
from datetime import datetime
from dateutil.relativedelta import relativedelta
from app.models.db import db
from app.models.transactions import TransactionModel
from app.models.transactions_splits import TransactionSplitModel

def ingest_transactions_data(csv_file_path):
    with open(csv_file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            # Create and add the transaction
            transaction = TransactionModel(
                date=datetime.strptime(row['date'], '%Y-%m-%d').date(),
                description=row['description'],
                installments=int(row['installments']),
                amount=float(row['amount']),
                payment_method=row['payment_method'],
                operation=row['operation'],
                user_id=int(row['user_id']),
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            db.session.add(transaction)
            db.session.flush()  # Ensure the transaction ID is available

            # Calculate and add the transaction splits
            installment_amount = transaction.amount / transaction.installments
            for i in range(transaction.installments):
                if i == 0:
                    installment_date = transaction.date
                else:
                    installment_date = (transaction.date + relativedelta(months=i)).replace(day=1)
                split = TransactionSplitModel(
                    transaction_id=transaction.id,
                    transaction_date=transaction.date,
                    installment_date=installment_date,
                    installment_number=i + 1,
                    total_amount=transaction.amount,
                    amount=installment_amount,
                    user_id=transaction.user_id,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.session.add(split)

        db.session.commit()