from flask import abort, jsonify, Blueprint, request
from ..models import ConfirmedOrder, Order
from . import api_bp
from .helper_auth import token_auth
from .errors import not_found
from .. import db_manager as db

@api_bp.route('/orders', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        new_order = Order(**data)
        db.session.add(new_order)
        db.session.commit()
        return jsonify({
            "success": True,
            "data": new_order.to_dict()
        }), 201

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
    try:
        order = Order.query.get(order_id)
        
        if not order:
            return jsonify({"error": "Not Found", "message": "Order not found", "success": False}), 404

        data = request.get_json()
        for key, value in data.items():
            setattr(order, key, value)
        db.session.commit()

        return jsonify({
            "success": True,
            "data": order.to_dict()
        }), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    try:
        order = Order.query.get(order_id)

        if not order:
            return jsonify({"error": "Not Found", "message": "Order not found", "success": False}), 404
    
        db.session.delete(order)
        db.session.commit()

        return jsonify({"success": True}), 200

    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

# Aceptar una oferta recibida
@api_bp.route('/orders/<int:order_id>/confirmed', methods=['POST'])
@token_auth.login_required
def confirm_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return not_found("Order not found")

    # Verificar que el usuario autenticado sea el "seller" del producto asociado a la orden
    if order.product.seller_id != token_auth.current_user().id:
        return jsonify({"error": "Forbidden", "message": "You are not the seller of this product", "success": False}), 403

    if order.confirmed:
        return jsonify({"error": "Bad Request", "message": "This offer has already been confirmed", "success": False}), 400

    order.confirmed = True
    db.session.commit()

    # Asegúrate de devolver el estado actualizado del pedido
    return jsonify({"success": True, "message": "Order confirmed successfully", "data": order.to_dict()})

# Anular una oferta aceptada
@api_bp.route('/orders/<int:order_id>/confirmed', methods=['DELETE'])
@token_auth.login_required
def cancel_confirmed_order(order_id):
    order = Order.query.get(order_id)

    if not order:
        return not_found("Order not found")

    # Verificar que el usuario autenticado sea el "seller" del producto asociado a la orden
    if order.product.seller_id != token_auth.current_user().id:
        return jsonify({"error": "Forbidden", "message": "You are not the seller of this product", "success": False}), 403

    if not order.confirmed:
        return jsonify({"error": "Bad Request", "message": "This offer has not been confirmed yet", "success": False}), 400

    db.session.delete(order)
    db.session.commit()

    # Devuelve un mensaje de éxito
    return jsonify({"success": True, "message": "Confirmed order canceled successfully"})