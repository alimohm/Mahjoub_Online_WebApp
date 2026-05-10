# core/__init__.py
from flask import Flask
from .extensions import db, login_manager 
# استيراد محرك الهوية لضمان التعرف على الجلسات (الموردين والموظفين)
from .setup import auth_loaders 

def create_app():
    # 1. تهيئة التطبيق وتحديد مسارات الواجهة (الترسانة الأم)
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # 2. تحميل الإعدادات السيادية من ملف Config
    app.config.from_object('config.Config')
    
    # 3. ربط المحركات الأساسية (Database & Auth)
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حماية الوصول وبوابة الدخول السيادية
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"
    login_manager.login_message_category = "info"

    with app.app_context():
        # 4. استيراد الموديلات من النقطة المركزية لضمان بناء الجداول
        from .models import User, Supplier, SupplierStaff
        
        # 5. بروتوكول تعميد وتحديث الجداول
        try:
            # بناء الجداول الجديدة إذا لم تكن موجودة
            db.create_all()
            
            # إصلاح يدوي للأعمدة المفقودة في PostgreSQL (حل مشكلة is_active و email)
            # هذا الكود يضمن استقرار السيرفر حتى لو كانت قاعدة Railway قديمة
            db.session.execute(db.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE"))
            db.session.execute(db.text("ALTER TABLE users ADD COLUMN IF NOT EXISTS email VARCHAR(150)"))
            db.session.execute(db.text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS email VARCHAR(150)"))
            db.session.execute(db.text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS identity_image VARCHAR(255)"))
            db.session.commit()
            
            print("✅ تم فحص وتحديث هيكل الجداول بنجاح (is_active & identities secured)")
        except Exception as e:
            print(f"⚠️ تنبيه أثناء تحديث الهيكل: {e}")
            db.session.rollback()

        # 6. تسجيل لوحة تحكم الإدارة (Blueprint)
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp) 
            print("✅ تم تسجيل لوحة التحكم بنجاح تحت مسار /admin")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل لوحة التحكم: {e}")

    return app
