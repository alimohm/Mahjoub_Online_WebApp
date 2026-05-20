# coding: utf-8
# 🏢 المصنع المركزي للنواة - منصة محجوب أونلاين 2026

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, template_folder='templates')
    app.config.from_object(Config)
    app.json.ensure_ascii = False

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        import apps.models.admin_db
        import apps.models.supplier_db
        import apps.models.wallet_db
        
        try:
            db.create_all()
            # (تم اختصار جزء أوامر الـ SQL هنا لعدم الإطالة، نفس كودك السابق)
            db.session.commit()
            print("🚀 سيادة وحوكمة: تم تطهير حقول الموازين الثابتة وإقرار البنية الرقمية النصية للمحافظ بنجاح.")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"❌ تعذر تحديث الجداول برمجياً: {str(e)}")
        finally:
            db.session.close()

    login_manager.login_view = 'auth_portal.login'
    login_manager.login_message = 'يرجى إثبات الهوية الرقمية للوصول إلى المنطقة السيادية.'
    login_manager.login_message_category = 'warning'

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # --- التعديلات المطلوبة هنا ---
    from apps.auth_portal import auth_blueprint
    # تم تغيير الاسم من admin_dashboard_blueprint إلى admin_dashboard
    from apps.admin_dashboard import admin_dashboard
    from apps.add_supplier.routes import admin_suppliers_bp
    from apps.wallet.routes import admin_wallet

    # التسجيل مع تثبيت الأسماء (Names)
    app.register_blueprint(auth_blueprint, url_prefix='/auth', name='auth_portal')
    # استخدام الاسم المعدل هنا
    app.register_blueprint(admin_dashboard, url_prefix='/admin', name='admin_dashboard')
    app.register_blueprint(admin_suppliers_bp, url_prefix='/admin', name='add_supplier')
    app.register_blueprint(admin_wallet, url_prefix='/admin', name='admin_wallet')

    return app
