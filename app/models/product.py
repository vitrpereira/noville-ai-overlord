from app.models.db import db, Base
import logging


class ProductModel(db.Model):
    __tablename__ = "products"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    updated_at = db.Column(db.DateTime, nullable=False)

logger = logging.getLogger("[ProductModel]")

class Product(Base):
    @classmethod
    def get_product_by_name(cls, product_name: str) -> ProductModel:
        return db.session.query(ProductModel).filter_by(name=product_name).first()
