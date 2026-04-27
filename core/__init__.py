import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية (النواة السيادية)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # 2. إنشاء كائن التطبيق
    app = Flask(__name__)

    # 3. الإعدادات السيادية (Configurations)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_9046_sovereign_key')
    
    # ربط قاعدة البيانات (دعم PostgreSQL للإنتاج و SQLite للتطوير)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. تهيئة الإضافات مع التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db) # تفعيل نظام التهجير لمنع انهيار السيرفر

    # إعدادات نظام الدخول
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة."
    login_manager.login_message_category = "info"

    # 5. تسجيل البوابات (Blueprints) داخل سياق التطبيق
    with app.app_context():
        # استيراد النماذج لضمان بناء الجداول السيادية
        from core import models
        
        # أ: تسجيل بوابة الموردين (Supplier Panel)
        from supplier_panel import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # ب: تسجيل بوابة الإدارة (Admin Panel) - مركز القيادة
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin_control_9046')
        except ImportError:
            # حماية في حال لم يتم رفع مجلد الإدارة بعد
            print("تنبيه: بوابة الإدارة لم ترفع بعد، سيتم تشغيل بوابة الموردين فقط.")

        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all()

    return app

# 6. إنشاء نسخة التطبيق النهائية للتشغيل (Gunicorn سيبحث عن كائن app)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
