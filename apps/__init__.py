from flask import Flask
import os
from models.admin_db import db  # تأكد من توحيد اسم الموديل المستخدم

def create_app():
    app = Flask(__name__)
    
    # الإعدادات السيادية للمنصة
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # معالجة رابط قاعدة البيانات ليتوافق مع Railway (PostgreSQL)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تهيئة قاعدة البيانات مع التطبيق
    db.init_app(app)

    # استيراد وتسجيل المحركات (Blueprints)
    # ملاحظة: نستورد البلوبرينت من المجلد مباشرة لضمان تشغيل __init__.py الخاص بكل تطبيق
    from .auth_portal.routes import auth_bp
    from .admin_dashboard import admin_dashboard
    from .add_supplier.routes import admin_suppliers
    
    # تسجيل البوابات الرقمية في هيكل النظام
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # إنشاء الجداول إذا لم تكن موجودة
    with app.app_context():
        db.create_all()

    return app
