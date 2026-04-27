import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية (خارج create_app لمنع مشاكل التكرار)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # 2. إنشاء كائن التطبيق
    app = Flask(__name__)

    # 3. الإعدادات السيادية (Configurations)
    # ملاحظة: تم تأمين المفاتيح والروابط مع قيم افتراضية للتطوير
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_9046_sovereign_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # إعدادات نظام الدخول الذكي
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النطاق المطلوب."
    login_manager.login_message_category = "info"

    # معالج محاولات الوصول غير المصرح بها للتوجيه الذكي
    @login_manager.unauthorized_handler
    def unauthorized():
        # إذا كان المستخدم يحاول دخول لوحة الإدارة، وجهه لصفحة دخول الأدمن
        if request.path.startswith('/admin_control_9046'):
            return redirect(url_for('admin_panel.admin_login'))
        # غير ذلك وجهه لصفحة دخول الموردين
        return redirect(url_for('supplier_panel.login'))

    # 5. تسجيل البوابات (Blueprints) داخل سياق التطبيق
    with app.app_context():
        # استيراد النماذج (Models) لضمان تسجيل الجداول
        try:
            from core import models
        except ImportError as e:
            print(f"⚠️ تنبيه: فشل استيراد النماذج: {e}")
        
        # أ: بوابة الموردين
        try:
            from supplier_panel import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
        except ImportError as e:
            print(f"⚠️ تنبيه: فشل تحميل بوابة الموردين: {e}")

        # ب: بوابة الإدارة - برج الرقابة المركزية
        try:
            # استدعاء admin_bp من حزمة admin_panel
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin_control_9046')
            print("✅ تم تفعيل بوابة الإدارة بنجاح")
        except (ImportError, AttributeError) as e:
            print(f"⚠️ تنبيه: فشل تحميل بوابة الإدارة: {e}")

        # إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
        db.create_all()

    return app

# 6. إنشاء نسخة التطبيق النهائية للتشغيل (Gunicorn سيبحث عن app)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    # استيراد محلي لتجنب التعارض (Circular Import)
    from core.models import User
    return User.query.get(int(user_id))
