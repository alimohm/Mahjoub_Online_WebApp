import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# تهيئة الإضافات (Extensions)
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    """
    دالة بناء التطبيق - المهندس والمحرك لمنصة محجوب أونلاين.
    """
    app = Flask(__name__)

    # إعدادات قاعدة البيانات والأمان من متغيرات بيئة Railway
    database_url = os.getenv("DATABASE_URL")
    
    # تصحيح الرابط ليتوافق مع SQLAlchemy 3 (تبديل postgres بـ postgresql)
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
        
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    # استخدام مفتاح الأمان السيادي الخاص بعلي محجوب
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Ali_Mahjoub_Sovereign_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تفعيل الإضافات داخل سياق التطبيق
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # إعدادات نظام الولوج السيادي
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "الدخول يتطلب صلاحيات القائد."

    with app.app_context():
        # --- التعديل الجوهري هنا ---
        # نستورد المجلد (Package) الذي يحتوي على تعريف البلوبرنت في __init__.py الخاص به
        from admin_panel import admin_panel as admin_blueprint
        app.register_blueprint(admin_blueprint, url_prefix='/admin')

        # استدعاء الموديلات لضمان بناء الجداول
        # ملاحظة: تأكد من وجود ملف __init__.py داخل مجلد models
        from core import models

    return app

@login_manager.user_loader
def load_user(user_id):
    """
    محرك التحقق من الهوية الرقمية.
    """
    from core.models.user import User
    return User.query.get(int(user_id))
