from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_cors import CORS  # استيراد المكتبة لدعم الاتصالات المتقاطعة
from config import Config

# تهيئة الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تفعيل CORS للمنصة
    # يسمح بالوصول لمسارات الـ admin من أي مصدر حالياً لتسهيل عمليات الربط
    CORS(app, resources={r"/admin/*": {"origins": "*"}})

    # ربط الإضافات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # إعدادات نظام تسجيل الدخول
    login_manager.login_view = 'admin.login'  # تم تعديله ليتوافق مع اسم الدالة في routes.py
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد النماذج (Models) لضمان تسجيلها في قاعدة البيانات
        from core.models.user import User
        
        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

        # تسجيل الـ Blueprints (لوحة التحكم الإدارية)
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # إنشاء الجداول إذا لم تكن موجودة (اختياري حسب بيئة العمل)
        # db.create_all() 

    return app
