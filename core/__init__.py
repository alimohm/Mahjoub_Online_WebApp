from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# إنشاء كائنات الإضافات (Extensions)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # --- الإعدادات السيادية (Configuration) ---
    # تأكد من ضبط متغير البيئة DATABASE_URL في Railway
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_secret_key_9046')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub_online.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # --- تهيئة الإضافات مع التطبيق ---
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)

    # إعدادات نظام تسجيل الدخول
    login_manager.login_view = 'supplier_panel.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة."
    login_manager.login_message_category = "info"

    with app.app_context():
        # استيراد النماذج (Models) هنا لضمان تسجيلها في قاعدة البيانات
        from core import models

        # استيراد وتسجيل البوابات (Blueprints)
        from supplier_panel import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # إنشاء الجداول إذا لم تكن موجودة (للتطوير الأولي)
        db.create_all()

    return app

# إنشاء نسخة التطبيق ليتم استدعاؤها في run.py أو gunicorn
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
