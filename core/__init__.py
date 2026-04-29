from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)

    # إعدادات التكوين
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'mahjoub_online_2026')
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///mahjoub.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin_panel.admin_login'

    with app.app_context():
        from admin_panel.routes import admin_bp
        from supplier_panel.routes import supplier_bp
        from core.models.user import User

        # تسجيل البلوبرينتس بمسارات واضحة
        app.register_blueprint(admin_bp, url_prefix='/admin')
        app.register_blueprint(supplier_bp, url_prefix='/supplier')

        db.create_all()

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    return app
