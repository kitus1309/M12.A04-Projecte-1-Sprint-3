from flask import Blueprint, jsonify
from ..models import Status  
from . import api_bp

@api_bp.route('/statuses', methods=['GET'])
def get_statuses():
    try:
        statuses = Status.query.all()
        return jsonify({
            "success": True,
            "data": [status.to_dict() for status in statuses]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
