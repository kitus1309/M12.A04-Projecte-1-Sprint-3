from flask import Blueprint, render_template, abort, flash, redirect, url_for
from .models import User, BlockedUser, Product, BannedProduct
from .helper_role import Role, role_required
from .forms import ConfirmForm, BlockUserForm, BanProductForm
from . import db_manager as db

# Blueprint
admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route('/admin')
@role_required(Role.admin, Role.moderator)
def admin_index():
    return render_template('admin/index.html')

@admin_bp.route('/admin/users')
@role_required(Role.admin)
def admin_users():
    users = User.get_all_with(BlockedUser)
    return render_template('admin/users/list.html', users=users)

@admin_bp.route('/admin/users/<int:user_id>/block', methods=["GET", "POST"])
@role_required(Role.admin)
def block_user(user_id):
    user = User.get(user_id)
    blocked = BlockedUser.get_filtered_by(user_id=user_id)

    if not user:
        abort(404)
    
    
    (user, blocked) = result


    (user, blocked) = result

    if blocked:
        flash("Compte d'usuari/a ja bloquejat", "error")
        return redirect(url_for('admin_bp.admin_users'))

    if user.is_admin_or_moderator():
        flash("Sols es poden bloquejar els usuaris wanner", "error")
        return redirect(url_for('admin_bp.admin_users'))

    form = BlockUserForm()
    if form.validate_on_submit():
        new_block = BlockedUser(user_id=user.id, message=form.message.data)
        new_block.create()
        flash("Compte d'usuari/a bloquejat", "success")
        return redirect(url_for('admin_bp.admin_users'))

    return render_template('admin/users/block.html', user=user, form=form)

@admin_bp.route('/admin/users/<int:user_id>/unblock', methods=["GET", "POST"])
@role_required(Role.admin)
def unblock_user(user_id):
    user = User.get(user_id)
    blocked = BlockedUser.get_filtered_by(user_id=user_id)

    if not user or not blocked:
        abort(404)
    
    
    (user, blocked) = result

    if not blocked:
        flash("Compte d'usuari/a no bloquejat", "error")
        return redirect(url_for('admin_bp.admin_users'))


    (user, blocked) = result

    if not blocked:
        flash("Compte d'usuari/a no bloquejat", "error")
        return redirect(url_for('admin_bp.admin_users'))

    if user.is_admin_or_moderator():
        flash("Sols es poden bloquejar els usuaris wanner", "error")
        return redirect(url_for('admin_bp.admin_users'))
    
    form = ConfirmForm()
    if form.validate_on_submit():
        blocked.delete()
        flash("Compte d'usuari/a desbloquejat", "success")
        return redirect(url_for('admin_bp.admin_users'))
    
    return render_template('admin/users/unblock.html', user=user, form=form)

@admin_bp.route('/admin/products/<int:product_id>/ban', methods=["GET", "POST"])
@role_required(Role.moderator)
def ban_product(product_id):
    product = Product.get(product_id)
    banned = BannedProduct.get_filtered_by(product_id=product_id)

    if not product:
        abort(404)

    if banned:
        flash("Producte ja prohibit", "error")
        return redirect(url_for('products_bp.product_list'))

    form = BanProductForm()
    if form.validate_on_submit():
        new_banned = BannedProduct(product_id=product.id, reason=form.reason.data)
        new_banned.create()
        flash("Producte prohibit", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/ban.html', product=product, form=form)

@admin_bp.route('/admin/products/<int:product_id>/unban', methods=["GET", "POST"])
@role_required(Role.moderator)
def unban_product(product_id):
    product = Product.get(product_id)
    banned = BannedProduct.get_filtered_by(product_id=product_id)
    
    if not product or not banned:
        abort(404)
    
    form = ConfirmForm()
    if form.validate_on_submit():
        banned.delete()
        flash("Producte permès", "success")
        return redirect(url_for('products_bp.product_list'))

    return render_template('admin/products/unban.html', product=product, form=form)
