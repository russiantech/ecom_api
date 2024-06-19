from datetime import datetime
from apis.ecommerce_api.factory import db
# from apis.products.models import Product
# from apis.users.models import User


class Basket(db.Model):
    __tablename__ = 'baskets'
    
    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='baskets')

    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    product = db.relationship('Product')

    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    deleted_at = db.Column(db.Boolean(), default=False)  # 0-deleted, 1-not-deleted
