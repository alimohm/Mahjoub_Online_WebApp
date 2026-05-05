from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # تسجيل الـ Blueprints هنا فقط لمنع الاستيراد الدائري
        from admin_panel import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        
        # إذا كان هناك ملف routes رئيسي للموقع (خارج الإدارة):
        # from . import routes 

    return app
