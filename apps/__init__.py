from flask import Flask
import os

def create_app():
    app = Flask(__name__)
    
    # إعدادات الأمان للمنصة
    app.config['SECRET_KEY'] = 'mahjoub_sovereign_2026'

    # 1. تشغيل محرك بوابة التحقق (Auth Engine)
    # القوالب موجودة داخل: apps/auth_portal/templates/
    from .auth_portal.routes import auth_bp
    app.register_blueprint(auth_bp)

    # 2. تشغيل محرك الموردين (Supplier Engine)
    # القوالب موجودة داخل: apps/add_supplier/templates/
    from .add_supplier.routes import admin_bp
    app.register_blueprint(admin_bp)

    # 3. تشغيل محرك لوحة التحكم (Dashboard Engine)
    # القوالب موجودة داخل: apps/admin_dashboard/templates/
    from .admin_dashboard.routes import dashboard_bp
    app.register_blueprint(dashboard_bp)

    return app
