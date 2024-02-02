from flask import abort, jsonify, Blueprint, request, g
from ..models import ConfirmedOrder, Order
from . import api_bp
from .. import db_manager as db
from .helper_auth import token_auth

@api_bp.route('/orders', methods=['POST'])
@token_auth.login_required
def create_order():
    data = request.get_json()
    if 'product_id' not in data:
        return jsonify({'error': 'Bad Request', 'message': 'Missing product_id', 'success': False}), 400

    product = Product.query.get(data['product_id'])
    if not product:
        return jsonify({'error': 'Not Found', 'message': 'Product not found', 'success': False}), 404

    if product.seller_id == g.current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'Cannot order your own product', 'success': False}), 403

    new_order = Order(buyer_id=g.current_user.id, **data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({
        "success": True,
        "data": new_order.to_dict()
    }), 201

@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
@token_auth.login_required
def update_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Not Found', 'message': 'Order not found', 'success': False}), 404
    
    if order.buyer_id != g.current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'Cannot modify an order that is not yours', 'success': False}), 403
    
    data = request.get_json()
    for key, value in data.items():
        setattr(order, key, value)
    db.session.commit()
    return jsonify({
        "success": True,
        "data": order.to_dict()
    }), 200

@api_bp.route('/orders/<int:order_id>', methods=['DELETE'])
@token_auth.login_required
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({'error': 'Not Found', 'message': 'Order not found', 'success': False}), 404

    if order.buyer_id != g.current_user.id:
        return jsonify({'error': 'Forbidden', 'message': 'Cannot delete an order that is not yours', 'success': False}), 403
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({'success': True}), 200

# Aceptar una oferta recibida
@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
def confirm_order(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            abort(404, description="Order not found")

        confirmed_order = ConfirmedOrder(order=order)
        db.session.add(confirmed_order)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Order {order_id} Confirmed successfully!"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Anular una oferta aceptada
@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
def cancel_confirmed_order(order_id):
    try:
        confirmed_order = ConfirmedOrder.query.filter_by(order_id=order_id).first()

        if not confirmed_order:
            abort(404, description=f"Order {order_id} not found")

        # Aquí podrías realizar validaciones adicionales antes de cancelar la orden confirmada

        db.session.delete(confirmed_order)
        db.session.commit()

        return jsonify({
            "success": True,
            "message": f"Order {order_id} Canceled successfully!"
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500