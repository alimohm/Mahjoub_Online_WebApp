import re
import random
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# إنشاء كائنات النظام الأساسية (العمود الفقري للترسانة الرقمية)
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- 1. إعدادات الأمان والتواصل (CORS) ---
    @app.after_request
    def add_cors_headers(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization'
        return response

    # --- 2. تهيئة المحركات الأساسية ---
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # حوكمة الدخول السيادية
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى النظام السيادي لـ محجوب أونلاين."
    login_manager.login_message_category = "info"

    # --- 3. تسجيل مركز القيادة (Blueprints) ---
    # نضعها هنا قبل الـ context لضمان تسجيلها فور بدء السيرفر
    from admin_panel import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    with app.app_context():
        # استيراد النماذج (Models) لضمان سلامة القاعدة
        from core.models.user import User
        try:
            from core.models.business import Order
        except ImportError:
            Order = None
        
        # إنشاء الجداول المفقودة تلقائياً
        try:
            db.create_all() 
        except Exception as e:
            print(f"⚠️ تنبيه حوكمة البيانات: تعذر تحديث الهيكل: {e}")

        # --- 4. المعالجات السياقية (بيانات الهوية) ---
        @app.context_processor
        def utility_processor():
            def get_sovereign_data():
                base_prefix = "MAH-963"
                rand_id = random.randint(1000, 9999)
                return {
                    "id": f"{base_prefix}{rand_id}", 
                    "wallet": f"W-{base_prefix}{rand_id}"
                }
            sov_data = get_sovereign_data()
            return dict(next_id=sov_data['id'], next_wallet=sov_data['wallet'])

    return app

# --- 5. إدارة جلسات المستخدمين (المحرك الخارجي لضمان عدم الانهيار) ---
@login_manager.user_loader
def load_user(user_id):
    from core.models.user import User
    try:
        # البحث المباشر عن المستخدم لضمان سرعة الاستجابة
        return db.session.get(User, int(user_id))
    except:
        return None
