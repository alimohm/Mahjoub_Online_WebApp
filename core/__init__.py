from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# 1. تعريف الكائنات المركزية (Global Objects)
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # إنشاء نسخة التطبيق وتحديد مسار الملفات الثابتة
    app = Flask(__name__, static_folder='../static')
    app.config.from_object(Config)
    
    # 2. تهيئة الإضافات (Initialize Extensions)
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات نظام الحماية
    login_manager.login_view = 'admin_panel.login'  # الصفحة التي يتم التحويل إليها إذا لم يسجل المستخدم دخوله
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى برج الرقابة المركزية"
    login_manager.login_message_category = "info"

    with app.app_context():
        try:
            # 3. استيراد المودلز (داخل الـ context لمنع الاستيراد الدائري)
            from core import models
            
            # تعريف دالة تحميل المستخدم لنظام الحماية
            @login_manager.user_loader
            def load_user(user_id):
                # يبحث أولاً في جدول المستخدمين (المدراء)
                return models.User.query.get(int(user_id))
            
            # 4. تسجيل البوابات (Blueprints)
            from admin_panel.routes import admin_bp
            from supplier_panel.routes import supplier_bp
            
            app.register_blueprint(admin_bp, url_prefix='/admin')
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [Core] تم تفعيل نظام الحماية وتسجيل جميع البوابات بنجاح.")
            
        except Exception as e:
            print(f"⚠️ [Core Error] حدث خطأ أثناء تهيئة الأنظمة: {e}")

    # 5. الواجهة الترحيبية للمنصة (Index Page)
    @app.route('/')
    def index():
        return """
        <div style="text-align:center; margin-top:50px; font-family: 'Cairo', sans-serif; direction:rtl; background: #050505; color: white; height: 100vh; display: flex; flex-direction: column; justify-content: center; align-items: center;">
            <h1 style="color: #D4AF37; font-size: 3rem; margin-bottom: 10px;">MAHJOUB | ONLINE</h1>
            <p style="color: #94a3b8; font-size: 1.2rem;">المحرك السيادي يعمل الآن بنظام الحماية المطور.</p>
            <div style="margin-top: 30px;">
                <a href="/admin/login" style="display:inline-block; padding:15px 40px; background: linear-gradient(135deg, #632C8F, #4a1d6d); color:white; text-decoration:none; border-radius:30px; font-weight:bold; border: 1px solid #D4AF37; box-shadow: 0 10px 20px rgba(99, 44, 143, 0.4); transition: 0.3s;">
                    دخول برج الرقابة ⬅️
                </a>
            </div>
            <p style="margin-top: 40px; font-size: 0.8rem; color: #4b5563;">&copy; 2026 جميع الحقوق محفوظة لـ محجوب أونلاين</p>
        </div>
        """

    return app
