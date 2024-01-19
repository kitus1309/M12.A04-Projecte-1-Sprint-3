from flask import request
from flask_login import current_user
from . import api_bp
from .errors import not_found, forbidden_access
from ..models import Product, Order
from .. import db_manager as db
from ..helper_json import json_response

# Listar productos y filtrar por título
@api_bp.route('/products', methods=['GET'])
def get_products():
    title = request.args.get('title')
    products = Product.get_all_filtered_by_title(title)
    data = [product.to_dict() for product in products]
    return json_response({"data": data, "success": True})

# Ver detalles de un producto
@api_bp.route('/products/<int:id>', methods=['GET'])
def get_product_details(id):
    product = Product.get(id)
    if product:
        data = product.to_dict()
        return json_response({"data": data, "success": True})
    else:
        return not_found("Product not found")

# Editar un producto propio
@api_bp.route('/products/<int:id>', methods=['PUT'])
def edit_product(id):
    product = Product.get(id)

    if not product:
        return not_found("Product not found")

    if product.seller_id != current_user.id:
        return forbidden_access("Unauthorized to edit this product")

    try:
        # Actualiza los campos según los datos proporcionados en la solicitud
        data = request.get_json()
        product.title = data.get('title', product.title)
        product.description = data.get('description', product.description)
        product.price = data.get('price', product.price)

        # Guarda los cambios en la base de datos
        db.session.commit()

        # Retorna la respuesta con los detalles actualizados del producto
        return json_response({"data": product.to_dict(), "success": True})

    except Exception as e:
        # En caso de error, puedes manejarlo y retornar un mensaje adecuado
        db.session.rollback()
        return json_response({"error": str(e), "success": False}, status=500)

# Llistar ofertes rebudes per un producte
@api_bp.route('/products/<int:id>/orders', methods=['GET'])
def get_product_orders(id):
    product = Product.get(id)
    if product:
        orders = Order.query.filter_by(product_id=id).all()
        data = [order.to_dict() for order in orders]
        return json_response({"data": data, "success": True})
    else:
        return not_found("Product not found")
