from datetime import datetime

from sqlalchemy import Column

from ecommerce_api.factory import db

users_roles = db.Table(
    'users_roles',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id')),
    keep_existing=True
)

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    users = db.relationship('User', secondary=users_roles, back_populates='roles')
    user_roles = db.relationship("UserRole", back_populates='role')
    
class UserRole(db.Model):
    __tablename__ = 'user_roles'

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))

    # # users = db.relationship("User", foreign_keys=[user_id], backref='roles')
    # user = db.relationship("User", foreign_keys=[user_id], backref='users_roles')
    # role = db.relationship("Role", foreign_keys=[role_id], backref='users_roles')

    user = db.relationship("User", foreign_keys=[user_id], back_populates='user_roles')
    role = db.relationship("Role", foreign_keys=[role_id], back_populates='user_roles')

    created_at = Column(db.DateTime, nullable=False, default=datetime.utcnow)
    __mapper_args__ = {'primary_key': [user_id, role_id]}

