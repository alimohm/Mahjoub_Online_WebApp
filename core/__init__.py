import os
from flask import Flask, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from werkzeug.middleware.proxy_fix import ProxyFix # أضف هذا السطر

# 1. تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # تحسين التعامل مع البروكسي في Render/Railway لضمان سلامة الروابط
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # 2. الإعدادات
    try:
        from config import Config
        app.config.from_object(Config)
    except ImportError:
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL') or 'sqlite:///mahjoub_online.db'
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub-secret-key-123'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 3. التهيئة
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # 4. إعدادات الدخول
    login_manager.login_view = 'admin_panel.admin_login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    # --- ⚓ المسار الافتراضي ⚓ ---
    @app.route('/')
    def index():
        return redirect(url_for('admin_panel.admin_login'))

    with app.app_context():
        # 5. استيراد الموديلات
        from core.models.user import User
        from core.models.product import Product
        from core.models.supplier import Supplier
        
        # إنشاء الجداول إذا لم تكن موجودة (بدون مسح القديم)
        db.create_all() 

        # 6. تسجيل البوابات (الـ Blueprints)
        try:
            from supplier_panel.routes import supplier_bp
            if 'supplier_panel' not in app.blueprints:
                app.register_blueprint(supplier_bp, url_prefix='/supplier')
        except Exception as e:
            app.logger.error(f"⚠️ خطأ بوابة الموردين: {e}")

        try:
            from admin_panel.routes import admin_bp 
            if 'admin_panel' not in app.blueprints:
                app.register_blueprint(admin_bp, url_prefix='/admin')
        except Exception as e:
            app.logger.error(f"⚠️ خطأ بوابة الإدارة: {e}")

        # 7. التعميد السيادي (لضمان وجود المستخدمين الأساسيين دائماً)
        try:
            if not User.query.filter_by(username="علي محجوب").first():
                admin_user = User(username="علي محجوب", role="admin", status="approved")
                admin_user.set_password("123")
                db.session.add(admin_user)
                db.session.commit()
                print("✅ تم تعميد حساب المدير بنجاح")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تعذر التعميد: {e}")

    return app

@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    # استخدام الطريقة الأحدث والمستقرة لجلب المستخدم
    return db.session.get(User, int(user_id))
