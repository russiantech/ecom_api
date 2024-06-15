from flask import request, jsonify
# from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import traceback
# from flask_wtf.csrf import csrf_exempt
from errors.response import bad_request

import sqlalchemy as sa

from ecommerce_api.factory import db, bcrypt #, csrf
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
def create_user():
    try:

        data = request.get_json()
        if 'username' not in data or 'email' not in data or 'password' not in data:
            return bad_request('must include username, email and password fields')

        if db.session.scalar(sa.select(User).where(
                User.username == data['username'])):
            return bad_request('please use a different username')

        if db.session.scalar(sa.select(User).where(
                User.email == data['email'])):
            return bad_request('please use a different email address')

        if 'phone' in data and db.session.scalar(sa.select(User).where(
                User.phone == data['phone'])):
            return bad_request('please use a different phone number')

        user = User()
        user.from_dict(data, new_user=True)
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
        # return user.to_dict(), 201, {'Location': url_for('api.get_user', id=user.id)}

    except Exception as e:
        print(traceback.print_exc())
        db.session.rollback()  # Rollback the transaction to maintain data integrity
        return jsonify({'error': f'User registration failed. {e}'}), 400
        
@blueprint.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        user = db.get_or_404(User, id)
        data = request.get_json()

        if 'username' in data and data['username'] != user.username and \
            db.session.scalar(sa.select(User).where(
                User.username == data['username'])):
            return bad_request('please use a different username')

        if 'email' in data and data['email'] != user.email and \
            db.session.scalar(sa.select(User).where(
                User.email == data['email'])):
            return bad_request('please use a different email address')

        user.from_dict(data, new_user=False)
        db.session.commit()
        
        return jsonify({'message': 'User updated successfully'}), 201

        # return user.to_dict()

    except Exception as e:
        print(traceback.print_exc())
        db.session.rollback()  # Rollback the transaction to maintain data integrity
        return jsonify({'error': f'User updation failed. {e}'}), 400


# go to> https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-xxiii-application-programming-interfaces-apis



@blueprint.route('/users_0', methods=['POST'])
def create_user_0():
    try:
        # Extract user registration data from the request
        name = request.json.get('name', None)
        username = request.json.get('username', None)
        email = request.json.get('email', None)
        phone = request.json.get('phone', None)
        password = request.json.get('password', None)

        # Retrieve the default role for a new user
        role = db.session.query(Role).filter_by(name='user').first()
        
        if role is None:
            default_role = Role(name='user')
            db.session.add(default_role)
            db.session.commit()

        # Hash the password before storing
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        # Create a new user instance and add to the database
        db.session.add(
            User(
            name=name, username=username, 
            email=email, phone=phone,
            password=hashed_password, 
            roles=[role]
            )
            )
        db.session.commit()

        return jsonify({'message': 'User registered successfully'}), 201
    except Exception as e:
        print(traceback.print_exc())
        db.session.rollback()  # Rollback the transaction to maintain data integrity
        return jsonify({'error': f'User registration failed. {e}'}), 400


@blueprint.route('/users/signin', methods=['POST'])
def signin():
    
    if not request.is_json:
        # return jsonify({"msg": f"Missing JSON in request -< {type(request.data.get('username'))} "}), 400
        return jsonify({"msg": "Missing JSON in request "}), 400

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

