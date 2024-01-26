from flask import Blueprint, jsonify, request
from .models import User, Product  # Assegura't que aquestes línies siguin correctes segons la teva estructura de projecte

api_bp = Blueprint('api_users', __name__)

@api_bp.route('/users', methods=['GET'])
def get_users():
    name_query = request.args.get('name', '')
    users = User.query.filter(User.name.contains(name_query)).all()
    return jsonify({
        "success": True,
        "data": [user.to_dict() for user in users]
    }), 200

@api_bp.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Not Found", "message": "User not found", "success": False}), 404
    return jsonify({
        "success": True,
        "data": user.to_dict()
    }), 200

@api_bp.route('/users/<int:user_id>/products', methods=['GET'])
def get_user_products(user_id):
    products = Product.query.filter_by(seller_id=user_id).all()
    return jsonify({
        "success": True,
        "data": [product.to_dict() for product in products]
    }), 200
