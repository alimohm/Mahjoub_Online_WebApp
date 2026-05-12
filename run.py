from flask import Flask
from core.extensions import db, login_manager
import os

def create_app():
    app = Flask(__name__)
    # إعدادات قاعدة البيانات
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = 'MAHJOUB_2026_SOVEREIGN'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    db.init_app(app)
    login_manager.init_app(app)

    # استدعاء محرك التأسيس داخل سياق التطبيق
    with app.app_context():
        from core.setup.initializer import initialize_sovereign_system
        initialize_sovereign_system(app)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
