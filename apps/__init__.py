# coding: utf-8
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 

# 1. تهيئة المحركات البرمجية خارج الدالة لضمان توفرها عالمياً
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth_portal.login'
login_manager.login_message = "وصول غير مصرح! يرجى تسجيل الدخول أولاً."
login_manager.login_message_category = "info"

def create_app():
    """
    دالة إنشاء التطبيق (App Factory) لربط كافة الأقسام البرمجية
    """
    app = Flask(__name__)
    
    # 2. الإعدادات البرمجية للمنصة
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # معالجة رابط قاعدة البيانات للبيئات السحابية (Railway)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. ربط المحركات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)

    # 4. محمل المستخدم (User Loader)
    # يربط الجلسة الحالية ببيانات المسؤول في قاعدة البيانات
    from apps.models.admin_db import AdminUser # تأكد من المسار والاسم الصحيح
    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # 5. تسجيل الأقسام البرمجية (Blueprints) من مجلد apps
    # نستخدم الاستيراد داخل الدالة لتجنب "الاستيراد الدائري"
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.add_supplier.routes import admin_suppliers
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 6. إنشاء الجداول في سياق التطبيق
    with app.app_context():
        try:
            db.create_all()
            print("✅ تم فحص وإنشاء جداول قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"❌ خطأ أثناء إنشاء الجداول: {e}")

    return app
