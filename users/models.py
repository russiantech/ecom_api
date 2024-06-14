from datetime import datetime

from ecommerce_api.factory import db, bcrypt
from roles.models import users_roles


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    phone = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password = db.Column(db.String(128))

    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', foreign_keys='Comment.user_id', back_populates='user', lazy='dynamic')
    # comments = db.relationship('Comment', foreign_keys='comment.user_id', backref='user', lazy='dynamic')

    roles = db.relationship('Role', secondary=users_roles, back_populates='users')
    user_roles = db.relationship("UserRole", back_populates='user')
    # roles = db.relationship('Role', secondary=users_roles, backref='users')

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def is_password_valid(self, password):
        return bcrypt.check_password_hash(self.password, password)

    def is_admin(self):
        return 'admin' in [r.name for r in self.roles]

    def is_not_admin(self):
        return not self.is_admin()
