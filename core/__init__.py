import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

load_dotenv()
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- إعدادات السيادة والأمان ---
    database_url = os.getenv("DATABASE_URL")
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "Mahjoub_Smart_Market_2026")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # تحصين الجلسات (Session Hardening)
    app.config['SESSION_COOKIE_SECURE'] = True    
    app.config['SESSION_COOKIE_HTTPONLY'] = True  
    app.config['REMEMBER_COOKIE_DURATION'] = 2592000 

    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد بوابة الدخول الافتراضية
    login_manager.login_view = 'supplier_panel.supplier_login'
    login_manager.login_message = "الدخول يتطلب تصريحاً سيادياً، يرجى تسجيل الدخول."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات أولاً لضمان تعريف الجداول في الترسانة
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier

        # تسجيل البوابات (Blueprints)
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        
        # التأكد من عدم وجود تعارض في البادئات (Prefixes)
        app.register_blueprint(admin_bp, url_prefix='/admin_central')
        app.register_blueprint(supplier_bp, url_prefix='/supplier_panel')

        # إنشاء الجداول إذا لم تكن موجودة (اختياري حسب بيئة التشغيل)
        # db.create_all() 

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    return User.query.get(int(user_id))
