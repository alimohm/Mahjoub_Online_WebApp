from flask import Flask
import os
# استيراد من مجلد models الموجود في جذر المشروع
from models.admin_db import db  

def create_app():
    app = Flask(__name__)
    
    # الإعدادات السيادية للمنصة
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY') or 'mahjoub_online_2026_key'
    
    # معالجة رابط قاعدة البيانات ليتوافق مع Railway
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # استيراد وتسجيل البلوبرينت
    from .auth_portal.routes import auth_bp
    from .admin_dashboard.routes import admin_dashboard
    from .add_supplier.routes import admin_suppliers
    
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    with app.app_context():
        db.create_all()

    return app
