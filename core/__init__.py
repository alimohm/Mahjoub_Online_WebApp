from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # الإعدادات
    app.config['SECRET_KEY'] = 'mahjoub_9046_key'
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///site.db')
    
    db.init_app(app)
    login_manager.init_app(app)

    # حماية من أخطاء الاستيراد: نسجل البلوبرنت هنا
    with app.app_context():
        # استيراد البلوبرنت من مجلد الموردين
        from supplier_panel import supplier_bp
        app.register_blueprint(supplier_bp, url_prefix='/supplier')
        
        # إنشاء الجداول
        from core import models
        db.create_all()

    return app

# إنشاء الكائن الذي سيستخدمه Gunicorn في Railway
app = create_app()

@login_manager.user_loader
def load_user(user_id):
    from core.models import User
    return User.query.get(int(user_id))
