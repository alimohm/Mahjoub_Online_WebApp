import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate

# 1. تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    # 2. إنشاء كائن التطبيق
    app = Flask(__name__)

    # 3. الإعدادات السيادية (Configurations)
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_9046_sovereign_key')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # إعدادات نظام الدخول
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النطاق المطلوب."
    login_manager.login_message_category = "info"

    # معالج التوجيه الذكي عند محاولة الدخول غير المصرح به
    @login_manager.unauthorized_handler
    def unauthorized():
        # إذا كان المسار يبدأ ببادرة الإدارة، وجهه لصفحة دخول الأدمن
        if request.path.startswith('/admin_control_9046'):
            return redirect(url_for('admin_panel.admin_login'))
        return redirect(url_for('supplier_panel.login'))

    # 5. تسجيل البوابات (Blueprints)
    with app.app_context():
        # استيراد قاعدة البيانات والنماذج
        from core import models
        
        # تسجيل بوابة الموردين
        try:
            from supplier_panel import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
        except ImportError as e:
            print(f"⚠️ تنبيه: فشل تحميل بوابة الموردين: {e}")

        # تسجيل بوابة الإدارة (مركز القيادة)
        try:
            # استيراد admin_bp من حزمة admin_panel
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin_control_9046')
            print("✅ تم تفعيل بوابة الإدارة بنجاح")
        except (ImportError, AttributeError) as e:
            # هذا الخطأ يظهر إذا كان admin_panel/__init__.py مفقوداً أو لا يحتوي على admin_bp
            print(f"❌ خطأ استيراد: فشل في العثور على admin_bp داخل مجلد الإدارة: {e}")

        # بناء الجداول السيادية
        db.create_all()

    return app

# 6. تشغيل التطبيق (النسخة التي يراها السيرفر)
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
