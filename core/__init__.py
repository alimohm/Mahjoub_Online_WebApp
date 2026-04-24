from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager # إضافة نظام إدارة الدخول
from config import Config
import os

# 1. تعريف الكائنات المركزية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    # 2. تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    
    # تحديد مسار صفحة الدخول الافتراضية
    login_manager.login_view = 'admin_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى برج الرقابة"
    login_manager.login_message_category = "info"

    with app.app_context():
        try:
            # 3. استيراد المودلز
            from core import models
            
            # تعريف دالة تحميل المستخدم (ضرورية لـ LoginManager)
            @login_manager.user_loader
            def load_user(user_id):
                return models.User.query.get(int(user_id))
            
            # 4. تسجيل البلوبرنت
            from admin_panel.routes import admin_bp
            from supplier_panel.routes import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ تم تفعيل أنظمة الحماية وتسجيل البوابات بنجاح.")
        except Exception as e:
            print(f"⚠️ تنبيه: تعذر تحميل بعض الأنظمة: {e}")

    # الصفحة الرئيسية الترحيبية
    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family: 'Cairo', sans-serif; direction:rtl;">
            <h1 style="color: #632C8F;">🚀 منصة محجوب أونلاين</h1>
            <p>المحرك السيادي يعمل الآن بنظام الحماية الجديد.</p>
            <div style="margin-top: 20px;">
                <a href="/admin/login" style="display:inline-block; padding:15px 30px; background:#632C8F; color:white; text-decoration:none; border-radius:25px; font-weight:bold; border: 1px solid #D4AF37;">
                    دخول برج الرقابة ⬅️
                </a>
            </div>
        </div>
        """

    return app
