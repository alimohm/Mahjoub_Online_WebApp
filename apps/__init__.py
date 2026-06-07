# coding: utf-8
# 📂 apps/__init__.py - المصنع الاحترافي المحصن (Render-Ready & Gunicorn-Compatible)

import os
import sys
from flask import Flask, redirect, url_for

# جعل مجلد الجذر مرئياً
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if base_dir not in sys.path:
    sys.path.insert(0, base_dir)

from apps.extensions import db, login_manager, migrate
from werkzeug.middleware.proxy_fix import ProxyFix

def safe_register(app_instance, module_path, attr_name, prefix):
    try:
        module = __import__(module_path, fromlist=[attr_name])
        blueprint = getattr(module, attr_name)
        app_instance.register_blueprint(blueprint, url_prefix=prefix)
    except Exception as e:
        print(f"⚠️ Failed to register {attr_name}: {e}")

# استخدام *args و **kwargs يجعل الدالة مرنة تماماً تجاه أي استدعاء من Gunicorn
def create_app(*args, **kwargs):
    app = Flask(__name__)
    
    # تحميل الإعدادات
    try:
        from config import Config
        app.config.from_object(Config)
    except:
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default-sovereign-key-2026')
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # إعدادات البروكسي
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # تسجيل النماذج
        from apps.models.admin_db import AdminUser
        from apps.models.supplier_db import Supplier
        from apps.models.wallet_db import SupplierWallet, WalletTransaction
        from apps.models.vault_db import AdminVault, VaultTransaction
        
        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id))

        # تسجيل المسارات
        safe_register(app, 'apps.auth_portal.routes', 'auth_portal
