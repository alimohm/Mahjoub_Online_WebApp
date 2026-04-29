import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# تحميل متغيرات البيئة
load_dotenv()

# تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- إعدادات الحوكمة الرقمية ---
    # تصحيح رابط قاعدة البيانات ليتوافق مع SQLAlchemy 2.0 في Render
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Mahjoub_Secret_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # مبادرة الكائنات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'supplier_panel.supplier_login'

    # --- تسجيل بوابات المنصة (Blueprints) ---
    # استيراد وتسجيل بوابة الإدارة
    from admin_panel.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # استيراد وتسجيل بوابة الموردين (شركاء النجاح)
    from supplier_panel.routes import supplier_bp
    app.register_blueprint(supplier_bp, url_prefix='/supplier')

    # استيراد الموديلات لضمان إنشاء الجداول
    with app.app_context():
        from . import models
        # db.create_all() # تفعيل هذا السطر عند أول تشغيل لإنشاء الجداول

    return app

# دالة لتحميل المستخدم (ضرورية لـ Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))
