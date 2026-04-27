import os
import sys
from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    login_manager.init_app(app)
    
    with app.app_context():
        # 1. استيراد الموديلات أولاً
        from core import models 
        
        # 2. استيراد البوابات محلياً داخل الدالة لمنع التعارض
        try:
            from admin_panel import admin_bp
            from supplier_panel import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ [Success] Blueprints registered.")
        except Exception as e:
            print(f"❌ [Error] Blueprint registration failed: {e}")

    return app
