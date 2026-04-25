from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية خارج الدالة لضمان توفرها في كامل النظام
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الملفات الثابتة والقوالب العامة
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام الحماية وتسجيل الدخول
    # المسار الافتراضي هو لوحة الإدارة؛ المورد سيتم التعامل معه داخل البلوبرنت الخاص به
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات هنا لمنع التعارض (Circular Import)
        from core import models
        
        # --- 🛡️ نظام التعرف الذكي على الهوية (أدمن أو مورد) ---
        @login_manager.user_loader
        def load_user(user_id):
            # أولاً: البحث في جدول الإدارة (الحسابات القيادية)
            admin = models.User.query.get(int(user_id))
            if admin:
                return admin
            
            # ثانياً: البحث في جدول الموردين (شركاء النجاح)
            return models.Supplier.query.get(int(user_id))

        # --- 🔗 تسجيل بوابات النظام (Blueprints) ---
        try:
            # تسجيل لوحة الإدارة المركزية
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين (نظام شركاء النجاح)
            # يتم استيراد البلوبرنت من ملف __init__ الخاص بالمجلد لضمان تحميل إعدادات القوالب
            from supplier_panel import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط جميع المسارات بنجاح: الإدارة (/) والموردين (/supplier)")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في تحميل بوابات النظام: {e}")

        # 4. تحديث وإنشاء جداول قاعدة البيانات (الموردين، المنتجات، الرصيد)
        db.create_all()
        
        print("🚀 [System] محجوب أونلاين في وضع الإقلاع الآن.")

    return app
