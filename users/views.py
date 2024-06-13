from flask import request, jsonify
# from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

# from flask_wtf.csrf import csrf_exempt


from ecommerce_api.factory import db, bcrypt, csrf
from roles.models import Role
from routes import blueprint
from shared.serializers import get_success_response
from users.models import User

@jwt_required(optional=True)
def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(loggeed_in_as='anonymous user'), 200

@blueprint.route('/users', methods=['POST'])
# @csrf_exempt
def create_user():
    try:
        # Extract user registration data from the request
        first_name = request.json.get('first_name', None)
        last_name = request.json.get('last_name', None)
        username = request.json.get('username', None)
        password = request.json.get('password', None)
        email = request.json.get('email', None)

        # Retrieve the default role for a new user
        role = db.session.query(Role).filter_by(name='ROLE_USER').first()

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance and add to the database
        db.session.add(User(first_name=first_name, last_name=last_name, username=username,
                            password=hashed_password, roles=[role], email=email))
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        db.session.rollback()  # Rollback the transaction to maintain data integrity
        return jsonify({'error': f'User registration failed. {e}'}), 400


@blueprint.route('/users/login', methods=['POST'])
def login():
    
    if not request.is_json:
        return jsonify({"msg": "Missing JSON in request"}), 400

    username = request.json.get('username', None)
    password = request.json.get('password', None)
    if username is None:
        return jsonify({"msg": "You must supply a username"}), 400
    if password is None:
        return jsonify({"msg": "Missing password parameter"}), 400

    user = User.query.filter_by(username=username).first()

    if user is None or not user.is_password_valid(str(password)):
        return jsonify({"msg": ""}), 401

    # Identity can be any data that is json serializable
    access_token = create_access_token(identity=user)

    return jsonify({
        'success': True,
        'user': {
            'username': user.username, 'id': user.id,
            'roles': [role.name for role in user.roles],
            'token': access_token}
    }), 200
