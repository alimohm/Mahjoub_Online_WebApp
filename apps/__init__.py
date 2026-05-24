# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # معالجة الـ Proxy لبيئات الإنتاج
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    with app.app_context():
        # استيراد الموديلات هنا فقط وبشكل مباشر
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet

        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

        # استيراد البلوبرينتس هنا فقط لكسر حلقة الاستيراد
        from apps.auth_portal.routes import auth_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.add_supplier.routes import admin_suppliers_bp
        from apps.wallet.routes import wallet_blueprint

        # تسجيل البلوبرينتس
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(admin_dashboard)
        app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

        # إنشاء الجداول
        db.create_all()

    return app

# لا تقم بإنشاء app = create_app() هنا إذا كان run.py يقوم بذلك
app = create_app()
