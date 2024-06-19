from apis.addresses.models import Address
from apis.categories.models import Category
from apis.comments.models import Comment
from apis.ecommerce_api.factory import app, db
from apis.file_uploads.models import FileUpload, ProductImage, TagImage, CategoryImage
from apis.orders.models import Order
from apis.products.models import Product
from routes import api_bp
from apis.errors.handlers import errors_bp
from apis.tags.models import Tag
from apis.users.models import User
from apis.chat.models import Chat

from views.products import static_bp

# Extensions, it is not how a well organized project initializes the extensions but hey, it
# is simple and readable anyways.

app.register_blueprint(api_bp, url_prefix='/api') #api-backend
app.register_blueprint(static_bp)  #api-frontend
# app.register_blueprint(errors_bp, url_prefix='/api/errors') //kukuma use/re-use a single bp
# app.config.setdefault("WTF_CSRF_CHECK_DEFAULT", False)

# Like the old school Flask-Script for the shell, but using the new Flask CLI which is way better
@app.shell_context_processor
def make_shell_context():
    return dict(
        app=app, db=db, User=User, address=Address, order=Order, product=Product,
        tag=Tag, category=Category, comment=Comment, file_upload=FileUpload, tag_image=TagImage,
        category_image=CategoryImage, product_image=ProductImage, chat=Chat,
        )


'''
Not used, to seed the database, it is as easy as running the seed_database.py python script
import click
import sys
@app.cli.command()
@click.option('--seed', default=None, help='seed the database')
def seed_db(value):
    sys.stdout.write('seed the database')
'''

if __name__ == '__main__':
    app.run(port=5001)
