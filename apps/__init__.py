# coding: utf-8
# 📂 apps/__init__.py - المصنع المحصن (النسخة النهائية المستقرة)

import os
from flask import Flask
from flask_migrate import Migrate
from flask_talisman import Talisman
from werkzeug.security import generate_password_hash
from apps.config import Config
from apps.extensions import db, login_manager, migrate
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
from apps.models.financial_db import ExchangeRate
from apps.models.vault_db import AdminVault

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🛡️ تحصين التطبيق
    Talisman(app, force_https=True, frame_options='SAMEORIGIN', referrer_policy='strict-origin-when-cross-origin')

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login'

    @login_manager.user_loader
    def load_user(user_id):
        return AdminUser.query.get(int(user_id))

    # تسجيل الـ Blueprints
    from apps.auth_portal.routes import auth_portal
    from apps.add_supplier.routes import add_supplier_bp
    from apps.admin_dashboard.routes import admin_dashboard
    from apps.wallet.routes import wallet_app
    from apps.vault.routes import vault_bp

    app.register_blueprint(auth_portal, url_prefix='')
    app.register_blueprint(add_supplier_bp, url_prefix='/suppliers')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(wallet_app, url_prefix='/wallet')
    app.register_blueprint(vault_bp, url_prefix='/vault')

    # تهيئة قاعدة البيانات الذكية (بدون حذف البيانات)
    with app.app_context():
        db.create_all() 
        
        try:
            # 1. إنشاء المدير فقط إذا كان الجدول فارغاً
            if not AdminUser.query.first():
                admin = AdminUser(username='علي_محجوب', role='Owner', phone_number='0000000000')
                admin.set_password('123')
                db.session.add(admin)
            
            # 2. إنشاء الخزينة إذا لم توجد
            if not AdminVault.query.first():
                db.session.add(AdminVault(balance_sar=0, balance_yer=0, balance_usd=0))
            
            # 3. زرع أسعار الصرف إذا كانت فارغة
            if not ExchangeRate.query.first():
                db.session.add(ExchangeRate(currency_code='USD', rate_to_sar=3.75))
                db.session.add(ExchangeRate(currency_code='YER', rate_to_sar=0.004))
            
            db.session.commit()
            print("✅ قاعدة البيانات جاهزة ومستقرة.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ خطأ أثناء التأسيس الآمن: {e}")

    return app
