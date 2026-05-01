from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from sqlalchemy import text

db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'admin.admin_login'

    # استيراد الموديلات هنا داخل الدالة لمنع الانهيار الدائري
    from core.models.user import User 
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # المرحلة 1: تنظيف القيود والترميم
        try:
            db.create_all()
            db.session.execute(text('ALTER TABLE users ALTER COLUMN password DROP NOT NULL;'))
            db.session.commit()
        except Exception:
            db.session.rollback()

        # المرحلة 2: الزرع القسري للقائد "علي محجوب"
        try:
            admin_user = User.query.filter_by(username="علي محجوب").first()
            if not admin_user:
                admin_user = User(username="علي محجوب", role='admin', is_active_account=True)
                admin_user.set_password('123')
                db.session.add(admin_user)
            else:
                admin_user.set_password('123')
                admin_user.is_active_account = True
            db.session.commit()
            print("✅ تم تأمين حساب القائد بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ خطأ في الزرع: {e}")

        # تسجيل المسارات
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    return app
