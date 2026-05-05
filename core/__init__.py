# core/__init__.py
from flask import Flask
from flask_login import LoginManager
from .extensions import db  # استدعاء db من الملف الجديد

login_manager = LoginManager()

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object('config.Config')
    
    # ربط الإضافات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # استدعاء الموديلات باستخدام الاستيراد النسبي
        from .models.user import User
        from .models.supplier import Supplier
        
        # تسجيل لوحة التحكم
        try:
            from admin_panel import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
        except ImportError:
            pass

        @login_manager.user_loader
        def load_user(user_id):
            return User.query.get(int(user_id))

    return app
