from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint
from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles
from apis.shared.custom_mixins import PaginatedAPIMixin


class Chat(db.Model, PaginatedAPIMixin):
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

