from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import CheckConstraint
from apis.ecommerce_api.factory import db, bcrypt
from apis.roles.models import users_roles
from apis.shared.custom_mixins import PaginatedAPIMixin

# UserGroup model (for many-to-many relationship between User and Group)
user_group = db.Table('user_group',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('group_id', db.Integer, db.ForeignKey('group.id'), primary_key=True)
)

class Chat(db.Model, PaginatedAPIMixin):
    from apis.users.models import User
    __tablename__ = 'chats'

    id = db.Column(db.Integer, unique=True, primary_key=True, nullable=False)

    text = db.Column(db.String(140))
    media = db.Column(db.String(140))
    sticker = db.Column(db.String(140))

    last_seen = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    fro_del = db.Column(db.Boolean(), default=False, nullable=False)
    to_del = db.Column(db.Boolean(), default=False, nullable=False)
    
    deleted = db.Column(db.Boolean(), default=False)
    created = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)
    updated = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    # Establish a foreign key relationship with the User model
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey(User.id), nullable=False)
    # user = db.relationship('User', backref='chats')  # Create a back reference
    user = db.relationship('User', back_populates='chats')
    # user = db.relationship('User', backref='chats', primaryjoin="Chat.user_id == User.id")

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


# MessageRecipient model (for individual and group messages)
class ChatRecipient(db.Model):
    __tablename__ = 'chatrecipients'
    id = db.Column(db.Integer, primary_key=True)
    chat_id = db.Column(db.Integer, db.ForeignKey('chat.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    # Add other fields as needed (e.g., is_read)

# Group model
class Group(db.Model):
    __tablename__ = 'groups'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    members = db.relationship('User', secondary='user_group', backref='groups')


""" class Chat(db.Model, PaginatedAPIMixin):
    __tablename__ = 'chats'

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


    fromuser_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    touser_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    
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