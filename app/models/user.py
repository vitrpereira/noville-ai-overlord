from app.models.db import db, Base
from datetime import datetime
import logging


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    phone_number = db.Column(db.String, nullable=False)
    name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)


logger = logging.getLogger("[UsersModel]")

class User(Base):

    @classmethod
    def register_user(
        cls, phone_number: str, name: str, product_id: int,
    ) -> str:
        logger.info(
            "[RegisterUser] Starting to register user"
        )

        try:
            user = UserModel(
                phone_number=phone_number,
                name=name,
                product_id=product_id,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )

            db.session.add(user)
            db.session.commit()

            logger.info(
                "[RegisterUser] Finished registering user"
            )

            return
        except Exception as exc:
            raise exc
    
    @classmethod
    def exists_by_phone_number_and_product_id(cls, phone_number: str, product_id: int) -> bool:
        logger.info(
            f"Checking if user exists in database: Phone Number: {phone_number} - Product ID: {product_id}"
            )

        if db.session.query(UserModel).filter_by(
            phone_number=phone_number,
            product_id=product_id
        ).first() is not None:
            logger.info(
                f"User with phone number: '{phone_number}' already registered for '{product_id}' product"
            )

            return True
        return False
