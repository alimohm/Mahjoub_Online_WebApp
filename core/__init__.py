from flask import Flask
from config import Config
from .models import db

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    with app.app_context():
        # استدعاء المسارات
        from admin_panel.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

        # إنشاء الجداول في قاعدة بيانات Render
        try:
            db.create_all()
            print("--- ✅ Database Tables Created ---")
        except Exception as e:
            print(f"--- ❌ DB Error: {str(e)} ---")

    return app
