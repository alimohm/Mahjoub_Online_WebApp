# coding: utf-8
# ملف: apps/__init__.py
# التوثيق: بناء المحرك الرئيسي للمنصة وتفعيل دروع الحماية

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect # 🛡️ الدرع المطلوب في ملف المتطلبات

# تهيئة الأدوات
db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    
    # 1. الإعدادات من ملف .env أو البيئة السحابية
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_secret_2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub.db')
    
    # 2. ربط الأدوات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # تفعيل درع الحماية لكل التطبيق

    # 3. تسجيل الأقسام (Blueprints)
    from apps.auth_portal.routes import auth_bp
    from apps.add_supplier.routes import admin_suppliers
    
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_suppliers, url_prefix='/suppliers')

    return app
