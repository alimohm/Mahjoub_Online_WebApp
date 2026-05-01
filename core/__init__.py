from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config
from sqlalchemy import text

# تعريف الأدوات المركزية للمنصة
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة الإضافات والربط مع قاعدة البيانات
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
        # --- المرحلة الأولى: ترميم الهيكل وحل نزاع القيود ---
        try:
            db.create_all()
            
            # تعطيل شرط الـ NOT NULL عن العمود القديم "password" لفتح الطريق أمام الزرع
            db.session.execute(text('ALTER TABLE users ALTER COLUMN password DROP NOT NULL;'))
            
            # التأكد من وجود الأعمدة الجديدة المطلوبة للهوية الحالية
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS username VARCHAR(150) UNIQUE;'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS password_hash VARCHAR(255);'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(20) DEFAULT \'admin\';'))
            db.session.execute(text('ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;'))
            
            db.session.commit()
            print("✅ تم تحرير قيود قاعدة البيانات وترميم الأعمدة بنجاح.")
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه أثناء الترميم (قد تكون القيود محررة بالفعل): {e}")

        # --- المرحلة الثانية: الزرع القسري للقائد (علي محجوب) ---
        try:
            target_name = "علي محجوب"
            admin_user = User.query.filter_by(username=target_name).first()
            
            if not admin_user:
                print(f"🚀 البدء في زرع الحساب السيادي: {target_name}")
                new_admin = User(
                    username=target_name,
                    role='admin',
                    is_active_account=True
                )
                # ملاحظة: set_password ستقوم بملء الحقلين لضمان القبول
                new_admin.set_password('123') 
                db.session.add(new_admin)
                db.session.commit()
                print(f"✅ تم زرع الحساب بنجاح. يمكنك الدخول الآن.")
            else:
                # تحديث دوري لضمان صلاحية البيانات
                admin_user.set_password('123')
                admin_user.role = 'admin'
                admin_user.is_active_account = True
                db.session.commit()
                print(f"ℹ️ حساب {target_name} نشط وجاهز للعمل.")
        
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ فشل الزرع مجدداً: {e}")

        # تسجيل Blueprints وتوجيه المسارات
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        @app.route('/')
        def index():
            return redirect(url_for('admin.admin_login'))

    return app
