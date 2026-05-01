from flask import Flask, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# تعريف الإضافات المركزية للمنصة
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # تهيئة الإضافات بربطها بمحرك التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # تحديد مسار الولوج السيادي لغير المسجلين
    # ملاحظة: 'admin.admin_login' تعتمد على اسم البلوبرنت المسجل أدناه
    login_manager.login_view = 'admin.admin_login'
    login_manager.login_message_category = 'info'

    # استيراد الموديل لتمكين نظام Flask-Login من التعرف على القائد (User)
    from core.models.user import User 
    
    @login_manager.user_loader
    def load_user(user_id):
        # استرجاع بيانات المستخدم من قاعدة البيانات المركزية بواسطة المعرف
        return User.query.get(int(user_id))

    with app.app_context():
        # استيراد وتسجيل بلوبرنت "برج الرقابة المركزية"
        # تم التأكد من مطابقة المسمى 'admin_bp' مع الملف admin_panel/routes.py
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        @app.route('/')
        def index():
            # توجيه تلقائي إلى بوابة الدخول لتركيز إدارة العمليات
            return redirect(url_for('admin.admin_login'))

    # إرجاع كائن التطبيق جاهزاً للتشغيل عبر run.py
    return app
with app.app_context():
    # استيراد البلوبرنت الذي يحتوي على المنطق والتعريف
    from admin_panel import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
