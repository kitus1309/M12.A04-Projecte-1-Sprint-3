from flask import request, jsonify
from . import api_bp
from .helper_auth import token_auth
from .errors import not_found
from ..models import Product, Order
from .. import db_manager as db

# Llistar productes i filtrar pel títol 
@api_bp.route('/products', methods=['GET'])
def get_products():
    name_query = request.args.get('title', '')
    products = Product.query.filter(Product.title.contains(name_query)).all()
    return jsonify({
        "success": True,
        "data": [product.to_dict() for product in products]
    }), 200

# Veure els detalls d’un producte
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product_details(id):
    product = Product.get(id)
    if product:
        data = product.to_dict()
        return jsonify({
            "success": True,
            "data": data
        }), 200
    else:
        return not_found("Product not found")

# Editar un producte propi
@api_bp.route('/products/<int:product_id>', methods=['PUT'])
@token_auth.login_required
def update_product(product_id):
    product = Product.query.get(product_id)

    if not product:
        return not_found("Product not found")

    # Verificar que el usuario autenticado sea el "seller" del producto
    if product.seller_id != token_auth.current_user().id:
        return jsonify({"error": "Forbidden", "message": "You are not the seller of this product", "success": False}), 403

    data = request.get_json()
    for key, value in data.items():
        setattr(product, key, value)
    db.session.commit()

    return jsonify({
        "success": True,
        "data": product.to_dict()
    }), 200

# Llistar ofertes rebudes per un producte
@api_bp.route('/products/<int:product_id>/orders', methods=['GET'])
def get_product_orders(product_id):
    product = Product.query.get(product_id)
    if not product:
        return not_found("Product not found")

    # Obtenemos las órdenes asociadas al producto
    orders = Order.query.filter_by(product_id=product.id).all()

    orders_details = [{
        "order_id": order.id,
        "buyer_id": order.buyer_id,
        "buyer_name": order.buyer.name,
        "offer": order.offer,
        "created": order.created
    } for order in orders]

    return jsonify({
        "success": True,
        "data": orders_details
    }), 200