from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

# تعريف الكائنات الأساسية
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # --- إعدادات التكوين (Configuration) ---
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_secret_key_2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- تهيئة الإضافات (Extensions) ---
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_panel.admin_login' # المسار الافتراضي عند عدم تسجيل الدخول
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- استيراد الموديلات والمسارات داخل السياق ---
        from core.models.user import User
        
        # استيراد البلوبرينتس من المجلدات التي وزعناها
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp

        # --- تسجيل البلوبرينتس (Registration) ---
        # استخدام url_prefix يمنع التداخل نهائياً
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # إنشاء قاعدة البيانات إذا لم تكن موجودة
        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
