# core/__init__.py
from flask import Flask
from flask_wtf.csrf import CSRFProtect # 🛡️ استيراد درع الحماية
from .extensions import db, login_manager 
from .setup import auth_loaders 

# تهيئة درع الحماية عالمياً
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__, 
                static_folder='../static', 
                template_folder='../templates')
    
    # تحميل الإعدادات (تأكد أن Config تحتوي على SECRET_KEY)
    app.config.from_object('config.Config')
    
    # --- تفعيل الترسانة الدفاعية والخدمات ---
    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app) # ✅ تعميد درع الحماية (هذا يحل خطأ csrf_token)
    
    login_manager.login_view = 'admin.login'
    login_manager.login_message = "يرجى تسجيل الدخول للوصول إلى الترسانة السيادية"

    with app.app_context():
        # 1. استيراد الموديلات المطهّرة من النقطة المركزية
        from .models import User, Supplier, SupplierStaff
        
        # 2. بروتوكول تحديث الجداول (PostgreSQL Migration)
        try:
            db.create_all()
            
            # تحديث حقول الموردين والمستخدمين (الخزينة الثلاثية والهوية الرقمية)
            # تم إضافة حقل permissions و full_name لضمان استقرار نظام الطاقم
            db_updates = [
                ("suppliers", "email", "VARCHAR(150)"),
                ("suppliers", "identity_image", "VARCHAR(255)"),
                ("suppliers", "balance_yer", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "balance_sar", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "balance_usd", "NUMERIC(20, 2) DEFAULT 0.0"), 
                ("suppliers", "sovereign_id", "VARCHAR(100) UNIQUE"),       
                ("suppliers", "tier", "VARCHAR(50) DEFAULT 'مبتدئ'"),
                ("users", "full_name", "VARCHAR(150)"),
                ("users", "permissions", "TEXT DEFAULT '{}'"),
                ("users", "role", "VARCHAR(50) DEFAULT 'admin'")
            ]
            
            for table, col_name, col_type in db_updates:
                try:
                    db.session.execute(db.text(f"ALTER TABLE {table} ADD COLUMN IF NOT EXISTS {col_name} {col_type}"))
                except Exception:
                    pass

            db.session.commit()
            
            # 3. بروتوكول التحقق من "القائد" وتعميد الهوية السيادية
            try:
                boss = Supplier.query.filter_by(trade_name="علي محجوب").first()
                if boss and not boss.sovereign_id:
                    boss.generate_sovereign_codes() 
                    db.session.commit()
                    print("✅ تم تعميد الهوية السيادية للقائد بنجاح.")
            except Exception as e:
                db.session.rollback()
                print(f"⚠️ تنبيه أثناء تعميد الهوية: {e}")

            print("✅ تم استكمال الترسانة وتطهير الهيكل بنجاح.")
            
        except Exception as e:
            print(f"⚠️ عطل سيادي في التهيئة: {e}")
            db.session.rollback()

        # 4. تسجيل لوحات التحكم (Admin Blueprint)
        # يتم الاستيراد هنا لتجنب الاستيراد الدائري (Circular Import)
        from admin_panel import admin_bp
        from admin_panel.staff_routes import staff_bp # تسجيل مسارات الطاقم
        
        app.register_blueprint(admin_bp) 
        # ملاحظة: staff_bp مسجل بالفعل داخل admin_panel/__init__.py 
        # ولكن نضمن هنا وعي التطبيق به.

    return app
