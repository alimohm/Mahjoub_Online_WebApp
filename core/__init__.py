import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # 2. جلب الإعدادات من ملف Config السيادي
    # تأكد أن ملف config.py موجود في المجلد الرئيسي للمشروع
    from config import Config
    app.config.from_object(Config)

    # 3. تهيئة الإضافات لربطها بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # تحديد الصفحة التي يتم التوجه إليها عند الحاجة لتسجيل الدخول (للإدارة كافتراضي)
    login_manager.login_view = 'admin_panel.admin_login'

    # 4. نظام التوجيه الذكي (حماية المسارات)
    @login_manager.unauthorized_handler
    def unauthorized():
        # إذا حاول شخص دخول صفحة محمية، يتم إرساله لبوابة الإدارة
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # استيراد النماذج (Models) لضمان ربط الجداول بقاعدة البيانات
        from core import models
        
        # 5. تسجيل البوابات (Blueprints) الموزعة في المجلدات المنفصلة
        
        # --- تسجيل بوابة الموردين (supplier_panel) ---
        try:
            from supplier_panel import supplier_bp
            # الرابط سيكون: /supplier/login
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ تم تفعيل بوابة الموردين بنجاح")
        except Exception as e:
            print(f"⚠️ بوابة الموردين واجهت مشكلة: {e}")

        # --- تسجيل بوابة الإدارة (admin_panel) ---
        try:
            from admin_panel import admin_bp 
            # الرابط سيكون: /admin/login (متوافق مع اسم المجلد والطلب)
            app.register_blueprint(admin_bp, url_prefix='/admin')
            print("✅ تم تفعيل بوابة الإدارة بنجاح")
        except Exception as e:
            print(f"⚠️ فشل تسجيل بوابة الإدارة: {e}")

        # إنشاء الجداول تلقائياً في قاعدة البيانات إذا لم تكن موجودة
        db.create_all()

    return app

# تحميل المستخدم من قاعدة البيانات بناءً على الـ ID الخاص به للجلسة
@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    try:
        return User.query.get(int(user_id))
    except:
        return None
