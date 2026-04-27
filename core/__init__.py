import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية للنظام
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 2. جلب الإعدادات من ملف config.py
    from config import Config
    app.config.from_object(Config)

    # 3. تهيئة الإضافات وربطها بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 4. تحديد "البوابة الافتراضية" التي يذهب إليها المستخدم غير المسجل
    # تم ربطها بـ admin_login لضمان التوجه لبرج الرقابة
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    @login_manager.unauthorized_handler
    def unauthorized():
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات (تأكد من وجود __init__.py داخل مجلد core/models)
        from core import models
        
        # 6. تسجيل بوابة الموردين (Supplier Panel)
        try:
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ تم تفعيل بوابة الموردين")
        except Exception as e:
            print(f"⚠️ فشل في بوابة الموردين: {e}")

        # 7. تسجيل بوابة الإدارة (Admin Panel - برج الرقابة 🏛️)
        try:
            # نستورد مباشرة من ملف routes لضمان العثور على الكائن admin_bp
            from admin_panel.routes import admin_bp 
            app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم تفعيل برج الرقابة المركزية بنجاح")
        except Exception as e:
            print(f"⚠️ فشل تسجيل بوابة الإدارة: {e}")

        # 8. إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
        db.create_all()

    return app

# 9. محمل المستخدم (User Loader) - المحرك الأساسي للتعرف على الهوية
@login_manager.user_loader
def load_user(user_id):
    # استيراد من المسار الدقيق للموديل لضمان عدم حدوث Unknown Location
    from core.models.user import User
    try:
        return User.query.get(int(user_id))
    except Exception as e:
        print(f"❌ خطأ في تحميل المستخدم: {e}")
        return None
