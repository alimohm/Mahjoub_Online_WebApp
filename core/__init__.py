from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسار الملفات الثابتة
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام تسجيل الدخول
    login_manager.login_view = 'admin_panel.login' # المسار الافتراضي عند محاولة دخول غير مصرح
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات لضمان تسجيلها في قاعدة البيانات
        from core import models
        
        # --- نظام التعرف على المستخدم (أدمن أو مورد) ---
        @login_manager.user_loader
        def load_user(user_id):
            # يحاول النظام أولاً البحث في جدول "القادة"
            admin = models.User.query.get(int(user_id))
            if admin:
                return admin
            # إذا لم يجد، يبحث في جدول "شركاء النجاح" (الموردين)
            return models.Supplier.query.get(int(user_id))

        # --- تسجيل بوابات النظام (Blueprints) ---
        
        # أ- لوحة الإدارة المركزية
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        # ب- بوابة الموردين (شركاء النجاح)
        try:
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            print("✅ [System] تم تسجيل بوابة الموردين بنجاح.")
        except Exception as e:
            print(f"⚠️ [Error] فشل في تسجيل بوابة الموردين: {e}")

        # 4. مزامنة الجداول مع قاعدة البيانات
        db.create_all()
        
        print("🚀 [System] محجوب أونلاين جاهز للإقلاع.")

    return app
