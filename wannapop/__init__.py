from flask import Flask, current_app
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_principal import Principal
from werkzeug.local import LocalProxy
from flask_debugtoolbar import DebugToolbarExtension
from .helper_mail import MailManager

# https://stackoverflow.com/a/31764294
logger = LocalProxy(lambda: current_app.logger)

db_manager = SQLAlchemy()
login_manager = LoginManager()
principal_manager = Principal()
mail_manager = MailManager()
toolbar = DebugToolbarExtension()

def create_app():
    # Construct the core app object
    app = Flask(__name__)

    # Llegeixo la configuració del config.py de l'arrel
    app.config.from_object('config.Config')

    # Inicialitza els plugins
    login_manager.init_app(app)
    db_manager.init_app(app)
    principal_manager.init_app(app)
    mail_manager.init_app(app)
    toolbar.init_app(app) # the toolbar is only enabled in debug mode
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    
    with app.app_context():
        from . import commands, routes_main, routes_auth, routes_admin, routes_products, routes_category, routes_status
        from .api import api_bp

        # Registra els blueprints
        app.register_blueprint(routes_main.main_bp)
        app.register_blueprint(routes_auth.auth_bp)
        app.register_blueprint(routes_admin.admin_bp)
        app.register_blueprint(routes_products.products_bp)
        app.register_blueprint(routes_category.category_bp)
        app.register_blueprint(routes_status.status_bp)
        
        # Registra comandes
        app.cli.add_command(commands.db_cli)

        # Registra el blueprint de l'API
        app.register_blueprint(api_bp, url_prefix='/api/v1.0')

    app.logger.info("Aplicació iniciada")

    return app