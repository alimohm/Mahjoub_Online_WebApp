# core/__init__.py
from flask import Flask
from .extensions import db, login_manager 
# استيراد محرك الهوية (Auth Loaders) لضمان التعرف على الجلسات
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
        # نستخدم الاستيراد من .models لضمان تفعيل ملف __init__.py هناك
        from .models import User, Supplier, SupplierStaff
        
        # 5. تعميد الجداول (بناء أو تحديث الهيكل في Railway)
        db.create_all()
        
        # 6. تسجيل لوحة تحكم الإدارة (Blueprint)
        try:
            # نستورد البلوبرنت من مجلد admin_panel مباشرة
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp) 
            print("✅ تم تسجيل لوحة التحكم بنجاح تحت مسار /admin")
        except Exception as e:
            print(f"⚠️ خطأ في تسجيل لوحة التحكم: {e}")

    return app
