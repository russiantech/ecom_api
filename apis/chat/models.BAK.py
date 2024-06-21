from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint
from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles
from apis.shared.custom_mixins import PaginatedAPIMixin

import sqlalchemy as sa
import sqlalchemy.orm as so

class Chat(db.Model):
    # from apis.users.models import User
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    sender_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('User.id'),
                                                 index=True)
    recipient_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey('User.id'),
                                                    index=True)
    body: so.Mapped[str] = so.mapped_column(sa.String(140))
    timestamp: so.Mapped[datetime] = so.mapped_column(
        index=True, default=lambda: datetime.now(timezone.utc))
    
    author: so.Mapped['User'] = so.relationship(
        foreign_keys='Chat.sender_id',
        back_populates='messages_sent')
    recipient: so.Mapped['User'] = so.relationship(
        foreign_keys='Chat.recipient_id',
        back_populates='messages_received')

    def __repr__(self):
        return '<Message {}>'.format(self.body)

""" class Chat(db.Model, PaginatedAPIMixin):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

    fromuser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    touser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    text = db.Column(db.String(140))
    media = db.Column(db.String(140))
    sticker = db.Column(db.String(140))

    seen = db.Column(db.Boolean(), default=False, nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    fro_del = db.Column(db.Boolean(), default=False, nullable=False)
    to_del = db.Column(db.Boolean(), default=False, nullable=False)
    
    deleted = db.Column(db.Boolean(), default=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    # Define the relationship with User
    # sender_user = db.relationship('User', foreign_keys=[fromuser_id])
    # receiver_user = db.relationship('User', foreign_keys=[touser_id])
    from_user = db.relationship('User', foreign_keys=[fromuser_id], back_populates='sent_messages')
    to_user = db.relationship('User', foreign_keys=[touser_id], back_populates='received_messages')
    __table_args__ = (
            CheckConstraint(
                "text IS NOT NULL OR sticker IS NOT NULL OR media IS NOT NULL",
                name="at_least_one_content_check",
            ),
        )
    
    def to_dict(self):
        data = {
            'id': self.id,
            **user, #unpacking
            'text': self.text if self.text else '',
            'sticker': self.sticker,
            'media': self.media,
            'seen': self.seen,
            'recent': self.recent,
            'last_message': self.text if self.text and self.recent else None,
            'fro_del': self.fro_del,
            'to_del': self.to_del,
            'created': self.created.isoformat() + 'Z' if self.created is not None else None,
            'updated': self.updated.isoformat() + 'Z' if self.updated is not None else None,
        }
        return data

    #microsoft's bing chat
    def from_dict(self, data, new_chat=False):
        if new_chat:
            for field in self.to_dict().keys():
                if field in data:
                    setattr(self, field, data[field])

    def __repr__(self):
        return '<Chat {}>'.format(self.text)
    # Remember to define the relationship between the `Chat` and `User` models.
 """


""" class Chat(db.Model, PaginatedAPIMixin):
    __tablename__ = 'chat'

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

    text = db.Column(db.String(140))
    media = db.Column(db.String(140))
    sticker = db.Column(db.String(140))

    seen = db.Column(db.Boolean(), default=False, nullable=False)
    last_seen = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    fro_del = db.Column(db.Boolean(), default=False, nullable=False)
    to_del = db.Column(db.Boolean(), default=False, nullable=False)
    
    deleted = db.Column(db.Boolean(), default=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)


    fromuser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    touser_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # fromuser_id = Column(Integer, ForeignKey('users.id'))
    # touser_id = Column(Integer, ForeignKey('users.id'))

    from_user = db.relationship('User', foreign_keys=[fromuser_id], back_populates='sent_messages')
    to_user = db.relationship('User', foreign_keys=[touser_id], back_populates='received_messages')

    __table_args__ = (
            CheckConstraint(
                "text IS NOT NULL OR sticker IS NOT NULL OR media IS NOT NULL",
                name="at_least_one_content_check",
            ),
        )


    def to_dict(self):
        data = {
            'id': self.id,
            **user, #unpacking
            'text': self.text if self.text else '',
            'sticker': self.sticker,
            'media': self.media,
            'seen': self.seen,
            'recent': self.recent,
            'last_message': self.text if self.text and self.recent else None,
            'fro_del': self.fro_del,
            'to_del': self.to_del,
            'created': self.created.isoformat() + 'Z' if self.created is not None else None,
            'updated': self.updated.isoformat() + 'Z' if self.updated is not None else None,
        }
        return data

    #microsoft's bing chat
    def from_dict(self, data, new_chat=False):
        if new_chat:
            for field in self.to_dict().keys():
                if field in data:
                    setattr(self, field, data[field])

    def __repr__(self):
        return '<Chat {}>'.format(self.text)
    # Remember to define the relationship between the `Chat` and `User` models.
 """
