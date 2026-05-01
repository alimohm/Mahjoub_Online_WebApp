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
    
    # تحديد بوابة الولوج السيادية لغير المسجلين
    # سيتم تحويل أي محاولة دخول غير مصرح بها إلى صفحة تسجيل دخول الإدارة
    login_manager.login_view = 'admin.admin_login'
    login_manager.login_message_category = 'info'

    # استيراد موديل المستخدم لتمكين نظام Flask-Login من التعرف على الهويات الرقمية
    from core.models.user import User 
    
    @login_manager.user_loader
    def load_user(user_id):
        # استرجاع بيانات المستخدم (قائد، مورد، أو عميل) بواسطة المعرف الفريد
        return User.query.get(int(user_id))

    with app.app_context():
        # استيراد وتسجيل بلوبرنت "برج الرقابة المركزية"
        # تم الربط مع المجلد admin_panel الذي يحتوي على المنطق والتعريف منفصلين
        from admin_panel import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # تسجيل بلوبرنت الموردين (VMS) - تأكد من إنشاء المجلد والملفات الخاصة به لاحقاً
        # from supplier_panel import supplier_bp
        # app.register_blueprint(supplier_bp, url_prefix='/supplier')

        @app.route('/')
        def index():
            # توجيه تلقائي للقادمين للمسار الرئيسي نحو بوابة الإدارة لتركيز إدارة العمليات
            return redirect(url_for('admin.admin_login'))

    # إرجاع كائن التطبيق جاهزاً للتشغيل عبر run.py
    return app
