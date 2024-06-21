from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

import sqlalchemy as sa
import sqlalchemy.orm as so

from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles
# from apis.products.models import products_users
from apis.pages.models import users_pages
from apis.chat.models import Chat

products_users = \
    db.Table(
        "products_users",
        db.Column("user_id", db.Integer, db.ForeignKey("user.id") ),
        db.Column("product_id", db.Integer, db.ForeignKey("products.id") )
        )

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    avater = db.Column(db.String(300))
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(120), index=True, unique=True)
    password = db.Column(db.String(128))
    about_me = db.Column(db.String(300))
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', foreign_keys='Comment.user_id', back_populates='user', lazy='dynamic')
    # comments = db.relationship('Comment', foreign_keys='comment.user_id', backref='user', lazy='dynamic')

    roles = db.relationship('Role', secondary=users_roles, back_populates='users')
    user_roles = db.relationship("UserRole", back_populates='user')
    # roles = db.relationship('Role', secondary=users_roles, backref='users')

    # Relationships with explicit primaryjoin conditions
    """ sent_messages = db.relationship('Chat', foreign_keys='Chat.fromuser_id', primaryjoin='Chat.fromuser_id == User.id', 
                                    backref='from_user', lazy='dynamic')
    received_messages = db.relationship('Chat', foreign_keys='Chat.touser_id', primaryjoin='Chat.touser_id == User.id', 
                                        backref='to_user', lazy='dynamic') """

    """ sent_messages: so.WriteOnlyMapped['Chat'] = so.relationship( foreign_keys='Chat.fromuser_id', back_populates='from_user')
    received_messages: so.WriteOnlyMapped['Chat'] = so.relationship(foreign_keys='Chat.touser_id', back_populates='to_user') """

    # sent_messages = db.relationship('Chat', foreign_keys=Chat.fromuser_id, back_populates='from_user', lazy='dynamic')
    # received_messages = db.relationship('Chat', foreign_keys=Chat.touser_id, back_populates='to_user', lazy='dynamic')
    # sent_messages = db.relationship('Chat', foreign_keys='Chat.fromuser_id', back_populates='from_user', lazy='dynamic')
    # received_messages = db.relationship('Chat', foreign_keys='Chat.touser_id', back_populates='to_user', lazy='dynamic')

     # Define the relationship with Chat using 'fromuser_id'
    # sent_messages = db.relationship('Chat', foreign_keys=Chat.fromuser_id, backref='from_user')
    # received_messages = db.relationship('Chat', foreign_keys=Chat.touser_id, backref='to_user')
    
    #sent_messages = db.relationship('Chat', foreign_keys='Chat.fromuser_id', backref='from_user')
    #received_messages = db.relationship('Chat', foreign_keys='Chat.touser_id', backref='to_user')

    messages_sent: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.sender_id', back_populates='author')
    messages_received: so.WriteOnlyMapped['Chat'] = so.relationship(
        foreign_keys='Chat.recipient_id', back_populates='recipient')

    baskets = db.relationship('Basket', back_populates='user')
    pages = db.relationship('Page', secondary=users_pages, lazy='dynamic', back_populates='users')
    products = db.relationship('Product', secondary=products_users, lazy='dynamic', back_populates='users')
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def from_dict(self, data, new_user=False):
        for field in ['username', 'avater', 'name', 'phone', 'email', 'about_me']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

        # Set default role for new user (assuming 'role_id' is provided in data)
        if new_user and 'role_id' in data:
            from apis.roles.models import Role  # Assuming Role model is imported here
            # user_role = db.session.query(Role).filter_by(id = data['role_id'] or name='user').first()
            user_role = db.session.query(Role).filter(
                (Role.id == data.get('role_id')) |
                (Role.name == 'user')
            ).first()

            if user_role:
                self.roles.append(user_role)

    def is_password_valid(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_admin(self):
        return 'admin' in [r.name for r in self.roles]

    def is_not_admin(self):
        return not self.is_admin()

    
    def __repr__(self):
        return '<User {}>'.format(self.username)

