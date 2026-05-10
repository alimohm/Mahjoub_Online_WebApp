# core/__init__.py
from flask import Flask
from .extensions import db, login_manager 
# استيراد محرك الهوية من المجلد الجديد لضمان تفعيله
from .setup import auth_loaders 

def create_app():
    # 1. تهيئة التطبيق وتحديد مسارات الواجهة
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # 2. تحميل الإعدادات السيادية من ملف Config
    app.config.from_object('config.Config')
    
    # 3. ربط المحركات الأساسية (Database & Auth)
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات حماية الوصول
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"
    login_manager.login_message_category = "info"

    with app.app_context():
        # 4. استيراد الموديلات لضمان تعريفها قبل إنشاء الجداول
        from .models.user import User
        from .models.supplier import Supplier
        
        # 5. تعميد الجداول (بناء قاعدة البيانات تلقائياً)
        db.create_all()
        
        # 6. تسجيل لوحة تحكم الإدارة (Blueprint) من مسارها الصحيح
        try:
            from admin_panel.routes import admin_bp
            # إضافة url_prefix='/admin' لضمان عمل الروابط بشكل سليم
            app.register_blueprint(admin_bp, url_prefix='/admin') 
            print("✅ تم تسجيل لوحة التحكم بنجاح تحت مسار /admin")
        except ImportError as e:
            print(f"⚠️ خطأ في تسجيل لوحة التحكم: {e}")

    return app
