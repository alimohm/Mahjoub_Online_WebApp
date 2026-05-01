from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# تعريف الأدوات المركزية
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة الإضافات
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    login_manager.login_view = 'admin.admin_login'
    login_manager.login_message_category = 'info'

    from core.models.user import User 
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    with app.app_context():
        # --- المرحلة الأولى: ترميم الجداول ---
        try:
            db.create_all() # إنشاء الجداول إذا لم تكن موجودة
            # ترميم الأعمدة لضمان التوافق مع تحديثات "علي محجوب"
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(150) UNIQUE;'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT \'admin\';'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;'))
            db.session.commit()
            print("✅ تم فحص وترميم أعمدة قاعدة البيانات بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه الترميم: {e}")

        # --- المرحلة الثانية: الزرع القسري للقائد (الحل الجذري) ---
        try:
            target_name = "علي محجوب"
            # البحث عن المستخدم
            admin_user = User.query.filter_by(username=target_name).first()
            
            if not admin_user:
                print(f"🚀 لم يتم العثور على القائد.. جاري زرع حساب: {target_name}")
                new_admin = User(
                    username=target_name,
                    role='admin',
                    is_active_account=True
                )
                new_admin.set_password('123')
                db.session.add(new_admin)
                db.session.commit()
                print(f"✅ تم زرع حساب {target_name} بنجاح كمسؤول نظام.")
            else:
                # تحديث كلمة المرور لضمان أنها 123 في حال حدوث أي خطأ سابق
                admin_user.set_password('123')
                admin_user.role = 'admin'
                admin_user.is_active_account = True
                db.session.commit()
                print(f"ℹ️ حساب {target_name} موجود بالفعل وتم تحديث صلاحياته وكلمة مروره.")
        
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ فشل زرع القائد في قلب النظام: {e}")

        # تسجيل Blueprints
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        @app.route('/')
        def index():
            return redirect(url_for('admin.admin_login'))

    return app
