import os
from flask import Flask, render_template
from config import Config
from core.models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # 1. تهيئة قاعدة البيانات
    db.init_app(app)

    # 2. تسجيل البوابات (داخل الدالة لضمان الترتيب)
    from admin_panel.routes import admin_bp
    from supplier_panel.routes import supplier_bp
    
    app.register_blueprint(admin_bp)
    app.register_blueprint(supplier_bp)

    # 3. محاولة إنشاء الجداول
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database connection waiting... {e}")

    @app.route('/')
    def index():
        return render_template('login.html')

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
