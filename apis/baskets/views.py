from flask import request, jsonify
# from flask_jwt_extended import create_access_token, jwt_optional, get_jwt_identity
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

import traceback
# from flask_wtf.csrf import csrf_exempt
from apis.errors.response import bad_request

import sqlalchemy as sa

from apis.ecommerce_api.factory import db, bcrypt #, csrf
from apis.roles.models import Role
from routes import api_bp
from apis.shared.serializers import get_success_response
from apis.users.models import User
from apis.product.models import Product

@jwt_required(optional=True)
def partially_protected():
    # If no JWT is sent in with the request, get_jwt_identity()
    # will return None
    current_user = get_jwt_identity()
    if current_user:
        return jsonify(logged_in_as=current_user), 200
    else:
        return jsonify(loggeed_in_as='anonymous user'), 200


@api_bp.route('/users', methods=['POST'])
def create_user():
    try:

        data = request.get_json()
        if 'username' not in data or 'email' not in data  or 'phone' not in data or 'password' not in data:
            return bad_request('must include username, email, phone and password fields')

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
        

@api_bp.route('/<string:action>/basket', methods=['GET', 'POST'])
def basket(action):
    
    item_id = str(request.args.get('item', ''))
    qty = int(request.args.get('qty', 1))
    
    basket = session.get('basket', {})

    try:
        if action == 'save':
            if Product.exists(item_id):
                basket[item_id] = basket.get(item_id, 0) + qty
                session['basket'] = basket
                session.modified = True
                return jsonify(message="Success, You've Added To Your Shopping Basket"), 200
            return jsonify(message="Failed! This Item Is Not Found"), 404
        
        elif action == 'update':
            if item_id in basket:
                basket[item_id] = qty
                session['basket'] = basket
                session.modified = True
                return jsonify(message="Success, You've Updated Your Shopping Basket"), 200
            elif Product.exists(item_id):
                basket[item_id] = qty
                session['basket'] = basket
                session.modified = True
                return jsonify(message="Success, You've Added And Updated Your Shopping Basket"), 200
            return jsonify(message="Failed, Unable To Update Your Shopping Basket"), 404
        
        elif action == 'remove':
            if item_id in basket:
                del basket[item_id]
                session['basket'] = basket
                session.modified = True
                return jsonify(message="Success, You've Removed An Item From Your Cart"), 200
            return jsonify(message="Sorry, Unable To Remove The Item From Your Shopping Cart"), 404
        
        elif action == 'wipe':
            session.pop('basket', None)
            session.modified = True
            return jsonify(message="You've Emptied Your Shopping Basket"), 200
        
        elif action == 'fetch':
            if not basket:
                return jsonify(message="Empty shopping basket"), 200

            items = Product.query.filter(Product.id.in_(basket.keys())).all()
            sub_total = sum(item.price * int(basket[str(item.id)]) for item in items)
            item_count = len(items)
            basket_items = [
                {
                    'item': item.id,
                    'name': item.name,
                    'image': item.photos,
                    'qty': basket[str(item.id)],
                    'price': item.price,
                    'total_each': item.price * int(basket[str(item.id)]),
                    'attr': item.attributes[0],
                }
                for item in items
            ]
            return jsonify(basket=basket_items, sub_total=sub_total, item_count=item_count), 200
        
        else:
            return jsonify(message="Invalid action"), 400

    except Exception as e:
        return jsonify(message=str(e)), 500
