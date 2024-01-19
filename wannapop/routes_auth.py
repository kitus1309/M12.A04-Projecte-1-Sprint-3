from flask import Blueprint, redirect, url_for, render_template, flash
from flask_login import current_user, login_required, login_user, logout_user
from . import login_manager, mail_manager, logger
from .forms import LoginForm, RegisterForm, ResendForm
from .helper_role import notify_identity_changed, Role
from .models import User
import secrets
from markupsafe import Markup

# Blueprint
auth_bp = Blueprint("auth_bp", __name__)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = LoginForm()
    if form.validate_on_submit():
        email = form.email.data
        password = form.password.data

        logger.debug(f"Usuari {email} intenta autenticar-se")

        user = User.get_filtered_by(email=email)
        if user and user.check_password(password):
            if not user.verified:
                logger.warning(f"Usuari {email} no s'ha autenticat correctament")
                flash("Revisa el teu email i verifica el teu compte", "error")
                return redirect(url_for("auth_bp.login"))
            
            logger.info(f"Usuari {email} s'ha autenticat correctament")

            login_user(user)
            notify_identity_changed()

            return redirect(url_for("main_bp.init"))

        flash("Error d'usuari i/o contrasenya", "error")
        return redirect(url_for("auth_bp.login"))
    
    return render_template('auth/login.html', form=form)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            email=form.email.data,
            password=form.password.data,
            role=Role.wanner,
            verified=False,
            email_token=secrets.token_urlsafe(20)
        )

        if new_user.create():
            logger.info(f"Usuari {new_user.email} s'ha registrat correctament")
            try:
                mail_manager.send_register_email(new_user.name, new_user.email, new_user.email_token)
                flash("Revisa el teu correu per verificar-lo", "success")
            except:
                logger.warning(f"No s'ha enviat correu de verificació a l'usuari/a {new_user.email}")
                flash(Markup("No hem pogut enviar el correu de verificació. Prova-ho més tard <a href='/resend'>aquí</a>"), "danger")
            return redirect(url_for("auth_bp.login"))
        else:
            logger.error(f"No s'ha inserit l'usuari/a {new_user.email} a BD")
            flash("Nom d'usuari/a i/o correu electrònic duplicat", "danger")
    
    return render_template('auth/register.html', form=form)

@auth_bp.route("/verify/<name>/<token>")
def verify(name, token):
    user = User.get_filtered_by(name=name, email_token=token)
    if user:
        user.verified = True
        user.email_token = None
        if user.update():
            flash("Compte verificat correctament", "success")
        else:
            flash("Error durant l'actualització del compte", "error")
    else:
        flash("Error de verificació", "error")
    return redirect(url_for("auth_bp.login"))

@auth_bp.route("/resend", methods=["GET", "POST"])
def resend():
    if current_user.is_authenticated:
        return redirect(url_for("main_bp.init"))

    form = ResendForm()
    if form.validate_on_submit():
        email = form.email.data
        user = User.get_filtered_by(email=email)
        if user and not user.verified:
            mail_manager.send_register_email(user.name, user.email, user.email_token)
            flash("Revisa el teu correu per verificar-lo", "success")
        else:
            flash("Aquest compte ja està verificat o no existeix", "error")
        return redirect(url_for("auth_bp.login"))
    else:
        return render_template('auth/resend.html', form=form)

@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("T'has desconnectat correctament", "success")
    return redirect(url_for("auth_bp.login"))

@login_manager.user_loader
def load_user(email):
    return User.get_filtered_by(email=email)

@login_manager.unauthorized_handler
def unauthorized():
    flash("Autentica't o registra't per accedir a aquesta pàgina", "error")
    return redirect(url_for("auth_bp.login"))
