from flask import Flask
from apps.extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    # استخدام app_context لكسر حلقة الاستيراد
    with app.app_context():
        # استيراد الموديلات والمسارات هنا فقط داخل سياق التطبيق
        from apps.auth_portal.routes import auth_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.add_supplier.routes import admin_suppliers_bp
        from apps.wallet.routes import wallet_blueprint

        # تسجيل المسارات (Blueprints)
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(admin_dashboard)
        app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')
        app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

        # إنشاء الجداول (اختياري، يفضل استخدامه مرة واحدة)
        # db.create_all()

    return app

# لا تقم بتعريف app = create_app() في أعلى الملف إذا كان run.py يقوم بذلك
