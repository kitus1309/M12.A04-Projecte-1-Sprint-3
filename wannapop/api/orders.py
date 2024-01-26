from flask import abort, jsonify
from . import api_bp
from ..models import ConfirmedOrder, Order
from .. import db_manager as db


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