from datetime import datetime

from slugify import slugify
from sqlalchemy import event, Column, Integer, ForeignKey, UniqueConstraint

from apis.ecommerce_api.factory import db

from datetime import datetime

from flask_jwt_extended import current_user
from slugify import slugify
from sqlalchemy import event
from sqlalchemy.orm import relationship

from apis.ecommerce_api.factory import db
from apis.categories.models import products_categories
from apis.tags.models import products_tags


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String, index=True, unique=True)
    description = db.Column(db.Text, nullable=False)

    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False)

    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    publish_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    tags = relationship('Tag', secondary=products_tags, backref='products')
    categories = relationship('Category', secondary=products_categories, backref='products')

    comments = relationship('Comment', backref='product', lazy='dynamic')

    def __repr__(self):
        return '<Product %r>' % self.name

    def __str__(self):
        return '<Product {}>'.format(self.name)

    def get_summary(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'stock': self.stock,
            'slug': self.slug,
            'comments_count': self.comments.count(),
            'tags': [{'id': t.id, 'name': t.name} for t in self.tags],
            'categories': [{'id': c.id, 'name': c.name} for c in self.categories],
            'image_urls': [i.file_path for i in self.images]
        }


@event.listens_for(Product.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(unicode(value))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    slug = db.Column(db.String(), index=True, unique=True)
    description = db.Column(db.String())
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime())

    def __repr__(self):
        return self.name

    def get_summary(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_urls': [image.file_path.replace('\\', '/') for image in self.images]
        }


@event.listens_for(Tag.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(unicode(value))


class ProductTag(db.Model):
    __tablename__ = 'products_tags'

    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=False)

    product = db.relationship("Product", foreign_keys=[product_id], backref='product_tags')
    tag = db.relationship("Tag", foreign_keys=[tag_id], backref='product_tags')

    __mapper_args__ = {'primary_key': [product_id, tag_id]}
    __table_args__ = (UniqueConstraint('product_id', 'tag_id', name='same_tag_for_same_product'),)


products_tags = db.Table(
    'products_tags',
    db.Column('product_id', db.Integer, db.ForeignKey('products.id')),
    db.Column('tag_id', db.Integer, db.ForeignKey('tags.id')),
    keep_existing=True
)

