from datetime import datetime
from flask_jwt_extended import current_user
from slugify import slugify
from sqlalchemy import event
from sqlalchemy.orm import relationship, backref

from apis.ecommerce_api.factory import db
from apis.categories.models import products_categories
from apis.tags.models import products_tags

class Product(db.Model):
    __tablename__ = 'products'
    __searchable__.BAK = [
        'name', 'price', 'description', 'currency', 'location', 'contact', 'user_id', 'pay_interval', 'condition',
        'negotiable', 'phone', 'about', 'required_skills', 'meet_up', 'ip', 'availability', 'company', 'sku', 'stock', 'discount', 'color', 'size', 'property_size',
        'model', 'year', 'make', 'job_level', 'min_experience', 'min_qualify', 'pay_range', 'responsibilities', 'job_setup', 'required_skills',
        'bedrooms', 'bathrooms', 'property_for', 'amenities', 'product_brand', 'address', 'date_available', 'product_type',
        'fuel_type'
    ]
    __searchable__ = [
        'name', 'price', 'description', 'currency', 'pay_interval', 'condition',
        'negotiable', 'phone', 'about', 'required_skills', 'meet_up', 'ip', 'availability', 'company', 'sku', 'stock', 'discount', 'color', 'size', 'property_size',
        'model', 'year', 'make', 'job_level', 'min_experience', 'min_qualify', 'pay_range', 'responsibilities', 'job_setup', 'required_skills',
        'bedrooms', 'bathrooms', 'property_for', 'amenities', 'product_brand', 'address', 'date_available', 'product_type',
        'fuel_type'
    ]

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    slug = db.Column(db.String(140), index=True, unique=True)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    stock = db.Column(db.Integer, nullable=False, default='1')
    
    # images = db.Column(db.JSON, nullable=False)

    currency = db.Column(db.String(50))
    pay_interval = db.Column(db.String(50)) # like monthly for product like property, commission-based for jobs/services
    negotiable = db.Column(db.Boolean(), default=False)
    product_type = db.Column(db.String(50), nullable=False, default='physical')
    product_brand = db.Column(db.String(50))
    condition = db.Column(db.String(50)) # (New, Used like new, Used good, Used fair)
    ip = db.Column(db.String(50))
    meet_up = db.Column(db.JSON)
    availability = db.Column(db.String(50)) # instock, single item, available, // updated to 'sold' if initially a single item and it's sold
    company = db.Column(db.String(50))

    # Product-specific fields
    sku = db.Column(db.String(1000), unique=True) # (stock keeping unit)
    discount = db.Column(db.Integer)
    color = db.Column(db.JSON, default=None, nullable=True) # color:- {'red','wine', 'etc'}
    size = db.Column(db.JSON, default=None, nullable=True) # size:- {'s','m', 'l', 'xl', 'xxl'}

    # Property/Real Estate fields
    property_size = db.Column(db.Integer)
    bedrooms = db.Column(db.Integer)
    bathrooms = db.Column(db.Integer)
    property_for = db.Column(db.String(50)) # [for rent/for sale]
    amenities = db.Column(db.JSON)
    date_available = db.Column(db.DateTime(timezone=True), default=datetime.utcnow)

    # Vehicle fields
    fuel_type = db.Column(db.String(50)) # [diesel, electric, gasoline, flex, hybrid, petrol, plug-in hybrid, other]
    make = db.Column(db.String(50))
    model = db.Column(db.String(50))
    year = db.Column(db.String(50))

    # Job fields
    job_level = db.Column(db.String(50)) # For job listings [senior, middle, leadership, junior]
    min_experience = db.Column(db.String(50), default='1') # minimum experience
    min_qualify = db.Column(db.String(50))
    pay_range = db.Column(db.Integer, default=None)
    responsibilities = db.Column(db.String(50))
    required_skills = db.Column(db.String(50))
    job_setup = db.Column(db.String(50)) # remote, office, hybrid

    location = db.Column(db.JSON, nullable=True) # location:- {'region':'USA', 'city':'london', 'street':'beach-house, 27 california', 'zipcode':'1099990'}
    contact = db.Column(db.JSON, nullable=True) # contact:- e.g., (name: name, email: email, phone: phone, etc)
    
    is_active = db.Column(db.Boolean(), default=True) # [sold, active]
    deleted_at = db.Column(db.Boolean(), default=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow, index=True, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    publish_on = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    # Foreign Keys and Relationships
    images = db.relationship('ProductImage', back_populates='product')
    users = db.relationship('User', secondary=products_users, lazy='dynamic', back_populates='products')
    pages = db.relationship('Page', secondary=products_pages, lazy='dynamic', back_populates='products')
    tags = db.relationship('Tag', secondary=products_tags, back_populates='products')
    categories = db.relationship('Category', secondary=products_categories, lazy='dynamic', back_populates='products')
    comments = db.relationship('Comment', back_populates='product', lazy='dynamic')

    def __repr__(self):
        return f'<Product {self.name}>'

    def __str__(self):
        return f'<Product {self.name}>'

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
            'image_urls': self.parse_json(self.images)
        }

    @staticmethod
    def parse_json(json_str):
        try:
            if json_str:
                return json.loads(str(json_str))
        except json.JSONDecodeError:
            return None

    @staticmethod
    def parse_str(str_val):
        try:
            if str_val is None or str_val == "":
                return None
            return str_val
        except AttributeError:
            return None
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'description': self.description,
            'stock': self.stock,
            'slug': self.slug,
            'comments_count': self.comments.count(),
            'tags': [{'id': t.id, 'name': t.name} for t in self.tags],
            'categories': [{'id': c.id, 'name': c.name} for c in self.categories],
            'image_urls': self.parse_json(self.images),
            'condition': self.condition,
            'currency': self.currency,
            'contact': self.parse_json(self.contact) if self.contact else None,
            'location': self.parse_json(self.location) if self.location else None,
            'color': self.parse_json(self.color) if self.color else None,
            'size': self.parse_json(self.size) if self.size else None,
            'meet_up': self.meet_up,
            'pay_interval': self.pay_interval,
            'negotiable': self.negotiable,
            'availability': self.availability,
            'product_type': self.product_type,
            'product_brand': self.product_brand,
            'sku': self.sku,
            'company': self.company,
            'discount': self.discount,
            'property_size': self.property_size,
            'bedrooms': self.bedrooms,
            'bathrooms': self.bathrooms,
            'property_for': self.parse_str(self.property_for),
            'date_available': self.date_available,
            'fuel_type': self.fuel_type,
            'make': self.make,
            'model': self.model,
            'year': self.year,
            'job_level': self.job_level,
            'min_experience': self.min_experience,
            'min_qualify': self.min_qualify,
            'pay_range': self.pay_range,
            'responsibilities': self.responsibilities,
            'required_skills': self.parse_str(self.required_skills),
            'job_setup': self.job_setup,
            'created_at': self.created_at,
            'updated_at': self.updated_at,
            'publish_on': self.publish_on,
            'page': {
                'id': self.pages.id if self.pages else None,
                'name': self.parse_str(self.pages.name) if self.pages else None,
                'desc': self.parse_str(self.pages.desc) if self.pages else None,
                'bank': self.parse_json(self.pagess.bank) if self.pages else None,
                'contact': self.parse_json(self.pages.contact) if self.pages else None,
                'location': self.parse_json(self.pages.location) if self.pages else None,
                'images': self.parse_json(self.pages.images) if self.pages else None,
                'socials': self.parse_json(self.pages.socials) if self.pages else None,
                'reviews': self.pages.reviews if self.pages else None,
                'page_user_id': self.pages.user_id if self.pages else None,
            },
            'user': {
                'page_url': None,
                'username': self.users.username if self.users else None,
                'location': self.users.location if self.users else None,
                'user_name': self.users.username if self.users else None,
            },
            '_links': {
                'user_profile': url_for('user_api.get_user', id=self.user_id) if self.user_id else None,
                'self': url_for('listing_api.get_listing', id=self.id),
            }
        }

    def from_dict(self, data, new_listing=False):
        for field in self.__searchable__:
            if field in data:
                setattr(self, field, data[field])
        if 'contact' in data:
            self.contact = json.dumps(data['contact'])
        if 'location' in data:
            self.location = json.dumps(data['location'])
        if 'images' in data:
            self.images = json.dumps(data['images'])
        if 'color' in data:
            self.color = json.dumps(data['color'])
        if 'size' in data:
            self.size = json.dumps(data['size'])
        if 'amenities' in data:
            self.amenities = json.dumps(data['amenities'])


@event.listens_for(Product.name, 'set')
def receive_set(target, value, oldvalue, initiator):
    target.slug = slugify(value)

