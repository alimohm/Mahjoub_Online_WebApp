import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تهيئة الإضافات الأساسية للمنصة
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- إعدادات البيئة (Railway & Postgres) ---
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        # تصحيح الرابط ليتوافق مع SQLAlchemy 2.0+
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # مفتاح الأمان السيادي الخاص بعلي محجوب
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Ali_Mahjoub_Sovereign_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تفعيل الملحقات داخل التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # تحديد صفحة تسجيل الدخول الافتراضية
    login_manager.login_view = 'admin_panel.admin_login'

    with app.app_context():
        # --- الحل الجذري لمشكلة الاستيراد ---
        # بدلاً من الاستيراد العام، نستورد كائن البلوبرنت بوضوح لتجنب تضارب الأسماء
        from admin_panel import admin_panel as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # استدعاء الموديلات لضمان بناء الجداول في قاعدة البيانات
        from core import models

    return app

# دالة تحميل المستخدم لمنصة محجوب أونلاين
@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
