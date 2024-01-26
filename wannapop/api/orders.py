from flask import Blueprint, jsonify, request
from ..models import Order, ConfirmedOrder  
from . import api_bp

@api_bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    new_order = Order(**data)
    db.session.add(new_order)
    db.session.commit()
    return jsonify({
        "success": True,
        "data": new_order.to_dict()
    }), 201

@api_bp.route('/orders/<int:order_id>', methods=['PUT'])
def update_order(order_id):
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

@api_bp.route('/orders/<int:order_id>', methods=['DELETE'])
def delete_order(order_id):
    order = Order.query.get(order_id)
    if not order:
        return jsonify({"error": "Not Found", "message": "Order not found", "success": False}), 404
    
    db.session.delete(order)
    db.session.commit()
    return jsonify({"success": True}), 200
