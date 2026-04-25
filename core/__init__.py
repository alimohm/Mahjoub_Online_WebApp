from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config
import os

# تهيئة الكائنات الأساسية خارج الدالة لضمان توفرها في كامل النظام
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    # 1. إنشاء نسخة التطبيق وتحديد مسارات الملفات الثابتة والقوالب العامة
    app = Flask(__name__, static_folder='../static', template_folder='../templates')
    app.config.from_object(Config)
    
    # 2. ربط المكتبات بالتطبيق
    db.init_app(app)
    login_manager.init_app(app)
    
    # 3. إعدادات نظام الحماية وتسجيل الدخول
    login_manager.login_view = 'admin_panel.login'  
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى هذه المنطقة السيادية."
    login_manager.login_message_category = "info"

    with app.app_context():
        # --- 🛡️ استيراد الموديلات المقسمة ---
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- 🔐 نظام التعرف الذكي على الهوية (أدمن أو مورد) ---
        @login_manager.user_loader
        def load_user(user_id):
            try:
                # أولاً: البحث في الحسابات القيادية (User)
                admin = User.query.get(int(user_id))
                if admin:
                    return admin
                
                # ثانياً: البحث في حسابات شركاء النجاح (Supplier)
                return Supplier.query.get(int(user_id))
            except Exception as e:
                print(f"⚠️ [Auth Error] فشل تحميل المستخدم: {e}")
                return None

        # --- 📊 نظام العدادات التلقائي (Context Processor) ---
        # هذا الجزء هو المسؤول عن ظهور رقم "طلبات الانتظار" في الـ Sidebar تلقائياً
        @app.context_processor
        def inject_global_data():
            try:
                # حساب عدد الموردين الذين ينتظرون الاعتماد
                p_suppliers = Supplier.query.filter_by(is_approved=False).count()
                # حساب عدد المنتجات التي تحتاج مراجعة (إذا كان لديك حقل مشابه)
                # p_products = Product.query.filter_by(is_approved=False).count() 
                return dict(pending_suppliers_count=p_suppliers)
            except:
                return dict(pending_suppliers_count=0)

        # --- 🔗 تسجيل بوابات النظام (Blueprints) ---
        try:
            # تسجيل لوحة الإدارة المركزية
            from admin_panel.routes import admin_bp
            app.register_blueprint(admin_bp, url_prefix='/admin')
            
            # تسجيل بوابة الموردين (نظام شركاء النجاح)
            # تم التأكد من استيراد المجلد الصحيح
            from supplier_panel.routes import supplier_bp
            app.register_blueprint(supplier_bp, url_prefix='/supplier')
            
            print("✅ [System] تم ربط جميع المسارات السيادية (الإدارة /admin + الموردين /supplier).")
        except Exception as e:
            print(f"❌ [Critical Error] فشل في تحميل بوابات النظام: {e}")

        # 4. مزامنة قاعدة البيانات
        db.create_all()
        print("🚀 [System] منصة محجوب أونلاين جاهزة للعمل بالهيكل الموزع.")

    return app
