# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    with app.app_context():
        # 1. تسجيل المحافظ
        from apps.wallet import wallet_blueprint
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

        # 2. 🔑 تسجيل بوابة المصادقة (هذا هو الأهم ليعمل رابط /auth/login)
        from apps.auth.routes import auth_blueprint 
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        # 3. تسجيل لوحة التحكم والموردين
        from apps.admin_dashboard.routes import admin_dashboard_blueprint
        app.register_blueprint(admin_dashboard_blueprint)
        
        # 4. تسجيل الموردين (تأكد من اسم الملف والـ Blueprint الخاص بهم)
        # from apps.suppliers.routes import add_supplier_blueprint
        # app.register_blueprint(add_supplier_blueprint, url_prefix='/suppliers')

        db.create_all()

    return app

app = create_app()
