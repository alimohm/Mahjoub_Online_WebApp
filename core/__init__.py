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
    
    # تصحيح مسار قاعدة البيانات لـ Railway/Render
    db_url = os.getenv("DATABASE_URL", "sqlite:///mahjoub.db")
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "MAHJOUB_2026_KEY")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- إضافات لمنع انهيار الجلسات ---
    app.config.update(
        SESSION_COOKIE_SECURE=True,    # تعمل فقط عبر HTTPS (رابط Railway)
        SESSION_COOKIE_HTTPONLY=True,  # تمنع اختراق الجلسة عبر JavaScript
        SESSION_COOKIE_SAMESITE='Lax', # توازن بين الأمان وسهولة الاستخدام
        REMEMBER_COOKIE_DURATION=2592000 # بقاء تسجيل الدخول لمدة 30 يوم
    )

    db.init_app(app)
    login_manager.init_app(app)
    
    # تخصيص رسائل الخطأ للجلسات
    login_manager.login_view = 'supplier_panel.supplier_login'
    login_manager.login_message = "يرجى تسجيل الدخول أولاً."
    login_manager.login_message_category = "info"

    with app.app_context():
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        return User.query.get(int(user_id))
    except:
        return None
