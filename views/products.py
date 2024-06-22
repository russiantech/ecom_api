from flask import request, jsonify, stream_template,  render_template
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import traceback
from apis.errors.response import bad_request
import sqlalchemy as sa
from apis.ecommerce_api.factory import db, app, bcrypt #, csrf
from apis.roles.models import Role
from views import static_bp
from apis.shared.serializers import get_error_response
from apis.users.models import User

@jwt_required(optional=True)
def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(loggeed_in_as='anonymous user'), 200


@app.route('/', methods=['GET'])
def listing():
    try:
        return stream_template('index.html')
        # return stream_template('index.html'), 201

    except Exception as e:
        print(traceback.print_exc())
        db.session.rollback()  # Rollback the transaction to maintain data integrity
        return jsonify({'error': f'products failed to load. {e}'}), 400
        

