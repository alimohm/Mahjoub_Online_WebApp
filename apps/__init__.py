# apps/__init__.py
from flask import Flask
from apps.extensions import db, login_manager
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. تهيئة الإضافات الأساسية
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    # 2. حماية الاستيرادات داخل السياق (هنا يكمن سر الحل)
    with app.app_context():
        # استيراد النماذج (Models) هنا فقط
        from apps.models.admin_db import AdminUser
        # (بقية الموديلات هنا)

        # استيراد وتسجيل المسارات (Blueprints)
        from apps.auth_portal.routes import auth_blueprint
        from apps.admin_dashboard.routes import admin_dashboard
        from apps.add_supplier.routes import admin_suppliers_bp
        
        app.register_blueprint(auth_blueprint, url_prefix='/auth')
        app.register_blueprint(admin_dashboard)
        app.register_blueprint(admin_suppliers_bp, url_prefix='/suppliers')

        # إنشاء الجداول (اختياري)
        db.create_all()

    return app

# ملاحظة: إذا كان ملف التشغيل الخارجي (run.py) يستدعي التطبيق، فلا تعرّف app هنا
app = create_app()
