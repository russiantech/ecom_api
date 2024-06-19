from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles
from apis.shared.custom_mixins import SearchableMixin

products_pages = \
    db.Table(
        "products_pages",
        db.Column("page_id", db.Integer, db.ForeignKey("pages.id") ),
        db.Column("product_id", db.Integer, db.ForeignKey("products.id") )
        )

users_pages = \
    db.Table(
        "users_pages",
        db.Column("user_id", db.Integer, db.ForeignKey("user.id") ),
        db.Column("page_id", db.Integer, db.ForeignKey("pages.id") )
        )

class Pages(db.Model, SearchableMixin):
    __tablename__ = 'pages'
    __searchable__ = ['name', 'username', 'email', 'phone', 'about']
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    desc = db.Column(db.Text, nullable=True)
    avater = db.Column(db.String(1000))
    socials = db.Column(db.JSON, default=None) # socials: { 'fb': '@chrisjsm', 'insta': '@chris', 'twit': '@chris','linkedin': '', 'whats':'@techa' }
    location = db.Column(db.JSON) #location:- {'region':'USA', 'city':'london', 'street':'beach-house, 27 california', 'zipcode':'1099990'},
    contact = db.Column(db.JSON) #contact:- see location column for sample using(emal:email,phone:phone,etc)
    bank = db.Column(db.JSON) #cmultiple({'opay':702656127, 'fcmb':5913408010})
    password = db.Column(db.String(500), index=True, nullable=False)
    reviews = db.Column(db.Integer)
    

    # user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    users = db.relationship('User',  secondary=users_pages, lazy='dynamic', back_populates='pages')
    products = db.relationship('Products',  secondary=products_pages, lazy='dynamic', back_populates='pages')

    deleted_at = db.Column(db.Boolean(), default= 0)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated_at = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

