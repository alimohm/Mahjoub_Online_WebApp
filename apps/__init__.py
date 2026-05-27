# coding: utf-8
import os
from flask import Flask
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager
from apps.utils.security import AESCipher

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # تهيئة التشفير
    app.cipher = AESCipher(app.config.get('ENCRYPTION_KEY', os.getenv('ENCRYPTION_KEY')))
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    with app.app_context():
        # استيراد الموديلات والمسارات هنا فقط لضمان عدم حدوث Circular Import
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet, WalletTransaction
        from apps.models.settlements_db import AdminSettlement
        from apps.models.statement_db import SupplierStatement 
        
        db.create_all() 

        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

        from apps.auth_portal.routes import auth_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.add_supplier.routes import admin_suppliers_bp
        from apps.financial_ops.routes import financial_blueprint 
        from apps.statement import statement_blueprint

        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(admin_dashboard)
        app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
        app.register_blueprint(financial_blueprint, url_prefix='/finance')
        app.register_blueprint(statement_blueprint, url_prefix='/statement')

    return app
