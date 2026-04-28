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

    # 4. إعدادات إدارة الدخول والوصول السيادي
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    @login_manager.unauthorized_handler
    def unauthorized():
        # التوجيه التلقائي لبرج الرقابة عند محاولة الدخول غير المصرح به
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات (لضمان بناء قاعدة البيانات بشكل سليم)
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier
        
        # 6. تسجيل بوابة الموردين (Supplier Panel)
        try:
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ تم تفعيل بوابة الموردين")
        except Exception as e:
            print(f"⚠️ تنبيه: بوابة الموردين لم تفعل بعد: {e}")

        # 7. تسجيل بوابة الإدارة (Admin Panel - برج الرقابة 🏛️)
        # تم تعديل الاستيراد هنا ليكون مباشراً من ملف routes لحل خطأ Unknown Location
        try:
            from admin_panel.routes import admin_bp 
            app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم تفعيل برج الرقابة المركزية بنجاح")
        except ImportError as e:
            print(f"❌ خطأ فادح في الاستيراد: {e}")
        except Exception as e:
            print(f"⚠️ خطأ عام في بوابة الإدارة: {e}")

        # 8. إنشاء الجداول في قاعدة البيانات
        db.create_all()

    return app

# 9. محمل المستخدم (User Loader) - المحرك الأساسي للتعرف على الهوية
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        # استخدام الطريقة الحديثة والمستقرة لجلب بيانات المستخدم
        return db.session.get(User, int(user_id))
    except Exception as e:
        print(f"❌ خطأ في نظام التحقق من الهوية: {e}")
        return None
