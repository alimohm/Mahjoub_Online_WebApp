from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد مسار صفحة الدخول (تأكد من كتابة admin_panel.login بدقة)
    login_manager.login_view = 'admin_panel.login'

    with app.app_context():
        from core import models
        
        @login_manager.user_loader
        def load_user(user_id):
            return models.User.query.get(int(user_id))
        
        # استيراد البلوبرنت
        from admin_panel.routes import admin_bp
        
        # تسجيل البلوبرنت مع الـ prefix
        # هذا السطر هو المسؤول عن جعل الرابط يبدأ بـ /admin
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        print("✅ [Routes] Admin Blueprint registered at /admin")

    return app
