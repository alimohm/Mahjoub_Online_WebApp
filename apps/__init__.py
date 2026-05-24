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

    db.init_app(app)
    login_manager.init_app(app)
    
    # ربط بوابة الدخول باسم البلوبرينت الصحيح 'auth_portal'
    login_manager.login_view = 'auth_portal.login' 

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    with app.app_context():
        # 1. تسجيل بلوبرينت المحافظ
        from apps.wallet.routes import wallet_blueprint
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

        # 2. تسجيل بلوبرينت المصادقة (بوابة الدخول)
        from apps.auth_portal.routes import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='/auth')

        # 3. تسجيل بلوبرينت لوحة التحكم
        from apps.admin_dashboard.routes import admin_dashboard
        app.register_blueprint(admin_dashboard)

        db.create_all()

    return app

# الإبقاء على كائن الدخول السيادي مستقراً في الخادم
app = create_app()
