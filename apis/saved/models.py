from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles


class Wishlist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    listing = db.relationship('Product., secondary=saved_listing, back_populates='saved', lazy='dynamic')

