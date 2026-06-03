# coding: utf-8
# 📂 apps/__init__.py - المصنع الرئيسي (التسجيل المباشر لضمان المسارات)

import os
from flask import Flask, redirect
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

# استيراد الـ Blueprints مباشرة لضمان التعرف عليها
from apps.auth_portal.routes import auth_portal
from apps.add_supplier.routes import add_supplier
from apps.financial_ops.routes import financial_blueprint
from apps.statement.routes import statement_blueprint
from apps.admin_dashboard.routes import admin_dashboard
from api.webhook import webhook_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # تهيئة قاعدة البيانات
        try:
            from apps.models.admin_db import AdminUser
            db.create_all()
        except Exception as e:
            print(f"❌ [Database Error]: {e}")

        @login_manager.user_loader
        def load_user(user_id):
            from apps.models.admin_db import AdminUser
            try: return AdminUser.query.get(int(user_id))
            except: return None

        # تسجيل المسارات بشكل مباشر (أكثر أماناً من الاستيراد الديناميكي)
        app.register_blueprint(auth_portal, url_prefix='')
        app.register_blueprint(add_supplier, url_prefix='/suppliers')
        app.register_blueprint(financial_blueprint, url_prefix='/financial_ops')
        app.register_blueprint(statement_blueprint, url_prefix='/statement')
        app.register_blueprint(admin_dashboard, url_prefix='/admin')
        app.register_blueprint(webhook_bp, url_prefix='')
        
        # 4. توجيه المسارات الأمنية
        @app.route('/')
        def root_redirect():
            secret_path = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')
            return redirect(secret_path)

        @app.route('/robots.txt')
        def robots_txt():
            return "User-agent: *\nDisallow: /", 200, {'Content-Type': 'text/plain'}

        @app.after_request
        def add_security_headers(response):
            response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive, nosnippet, noimageindex"
            response.headers["X-Frame-Options"] = "DENY"
            response.headers["X-Content-Type-Options"] = "nosniff"
            return response

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
