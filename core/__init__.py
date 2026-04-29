import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

# تحميل الإعدادات
load_dotenv()

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # إعدادات قاعدة البيانات والتوافق مع Render
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Mahjoub_Smart_Market_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # مبادرة المكتبات
    db.init_app(app)
    login_manager.init_app(app)
    
    # صفحة الدخول الافتراضية عند محاولة الوصول لصفحة محمية
    login_manager.login_view = 'admin_panel.admin_login'

    with app.app_context():
        # تسجيل بوابة الإدارة (التي سنقوم بتشغيلها الآن)
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # تسجيل بوابة الموردين (التي تعمل لديك حالياً)
        from supplier_panel.routes import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # استيراد الموديلات
        from . import models

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))
