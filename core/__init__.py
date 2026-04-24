from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية خارج الدالة لضمان توفرها في كامل النظام
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الملفات الثابتة والقوالب
    # ملاحظة: تركنا القوالب عامة هنا لأن كل Blueprint سيحدد مجلده الخاص
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام الحماية وتسجيل الدخول
    # المسار الافتراضي (للأدمن) - المورد سيتم توجيهه برمجياً في الـ routes الخاصة به
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد الموديلات هنا لمنع الـ Circular Import
        from core import models
        
        # --- نظام التعرف الذكي على نوع المستخدم (أدمن أو مورد) ---
        @login_manager.user_loader
        def load_user(user_id):
            # محاولة البحث في جدول الإدارة أولاً
            user = models.User.query.get(int(user_id))
            if user:
                return user
            # إذا لم يجد، يبحث في جدول الموردين (Supplier)
            return models.Supplier.query.get(int(user_id))

        # --- تسجيل بوابات النظام (Blueprints) ---
        
        try:
            # تسجيل لوحة الإدارة
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين (شركاء النجاح)
            # تأكد أن البلوبرنت في ملفه الخاص (supplier_panel/__init__.py) 
            # يحتوي على template_folder='templates'
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط جميع البوابات بنجاح (الإدارة + الموردين).")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في تحميل أحد المسارات: {e}")

        # 4. تحديث/إنشاء قاعدة البيانات آلياً
        db.create_all()
        
        print("🚀 [System] منصة محجوب أونلاين في وضع الاستعداد التام.")

    return app
