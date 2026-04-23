from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        # تسجيل الصفحات (Blueprints)
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        # إنشاء الجداول فوراً عند تشغيل السيرفر
        db.create_all()
        print("--- ✅ Database Connected & Tables Created ---")

    return app
