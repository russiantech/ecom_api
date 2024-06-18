from flask import Blueprint
# from apis.ecommerce_api.factory import csrf

api_bp = Blueprint('api', __name__)

# static_bp = Blueprint('static_bp', __name__)

# csrf.exempt(api_bp) # disable csrf-protection to fix error-400(BAD REQUEST)