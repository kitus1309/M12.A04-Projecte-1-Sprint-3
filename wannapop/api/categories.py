from flask import jsonify
from ..models import Category  
from . import api_bp

@api_bp.route('/categories', methods=['GET'])
def get_categories():
    try:
        categories = Category.query.all()
        return jsonify({
            "success": True,
            "data": [category.to_dict() for category in categories]
        }), 200
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500