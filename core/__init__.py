from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# --- 🛡️ تهيئة الترسانة البرمجية الأساسية ---
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الموارد
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بنواة التطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. بروتوكولات الحماية وتسجيل الدخول الافتراضية
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى إثبات هويتك للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- 📦 استيراد النماذج (Models) داخل السياق لمنع التداخل ---
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- 🔐 نظام الفصل الذكي بين الهويات (Advanced Multi-Auth) ---
        @login_manager.user_loader
        def load_user(user_id):
            try:
                user_type = session.get('user_type')
                if user_type == 'supplier':
                    return Supplier.query.get(int(user_id))
                return User.query.get(int(user_id))
            except Exception as e:
                return None

        # --- 🔗 تسجيل بوابات النظام (Blueprints Registration) ---
        try:
            # 1. بوابة الإدارة المركزية (برج الرقابة)
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # 2. بوابة الموردين (التصحيح هنا)
            # نستورد البلوبرنت من المجلد مباشرة لأننا عرفناه في __init__.py الخاص بالمجلد
            from supplier_panel import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم تفعيل بوابة الموردين على المسار /supplier بنجاح.")
        except Exception as e:
            print(f"❌ [Critical Error] خطأ في ربط بوابات النظام: {e}")

        # --- 📊 معالج البيانات الشامل (Context Processor) ---
        @app.context_processor
        def inject_global_data():
            try:
                p_suppliers = Supplier.query.filter_by(is_approved=False).count()
                return dict(pending_suppliers_count=p_suppliers)
            except Exception:
                return dict(pending_suppliers_count=0)

        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all()

    return app
