from datetime import datetime
from slugify import slugify
from sqlalchemy import event, ForeignKey
from sqlalchemy.orm import relationship, backref
from apis.ecommerce_api.factory import db
# from apis.products.models import products_categories

products_categories = \
    db.Table(
        "products_categories",
        db.Column("category_id", db.Integer, db.ForeignKey("categories.id") ),
        db.Column("product_id", db.Integer, db.ForeignKey("products.id") )
        )

class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(140))
    slug = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime())
    
    products = db.relationship('Product', secondary=products_categories, lazy='dynamic', back_populates='categories')
    # Self-referential relationship + nested categorization using same table.
    parent_id = db.Column(db.Integer, ForeignKey('categories.id'), nullable=True)
    parent = db.relationship('Category', remote_side=[id], backref=backref('children', lazy='dynamic'))
    
    def get_summary(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'image_urls': [image.file_path.replace('\\', '/') for image in self.images],
            'children': [child.get_summary() for child in self.children]
        }

    def __repr__(self):
        return self.name

@event.listens_for(Category.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(value)  # Removed unicode() as it is not necessary in Python 3


