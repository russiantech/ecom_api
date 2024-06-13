from flask import Blueprint
from ecommerce_api.factory import csrf

blueprint = Blueprint('main', __name__)

csrf.exempt(blueprint) # disable csrf-protection to fix error-400(BAD REQUEST)