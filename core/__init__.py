from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # إنشاء التطبيق (تلقائياً سيبحث عن المجلدات الفرعية للبلوبرينت)
    app = Flask(__name__)
    
    # تحميل الإعدادات من ملف config.py الخارجي
    app.config.from_object('config.Config')

    # تهيئة قاعدة البيانات ونظام الدخول
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_panel.admin_login'

    with app.app_context():
        # تسجيل بوابة الإدارة (برج الرقابة)
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # تسجيل بوابة الموردين
        from supplier_panel.routes import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # استيراد الموديلات وإنشاء الجداول
        from core.models.user import User
        db.create_all()

    @app.route('/')
    def index():
        return redirect(url_for('admin_panel.admin_login'))

    return app
