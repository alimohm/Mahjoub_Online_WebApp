# run.py
import os
import logging
from sqlalchemy import text
from core import create_app, db
from core.models.user import User
from core.models.supplier import Supplier

# استيراد البلوبرنتات لضمان تسجيلها في المحرك الرئيسي
from admin_panel.routes import admin_bp 
from admin_panel.staff_routes import staff_bp

# إعداد السجلات السيادية لمركز العمليات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("Mahjoub_System")

# 1. تهيئة التطبيق المركزي
app = create_app()

# 2. تسجيل لوحات التحكم (Blueprints)
if not app.blueprints.get('admin'):
    app.register_blueprint(admin_bp, url_prefix='/admin')
    logger.info("📡 تم تفعيل مسارات لوحة التحكم تحت /admin")

if not app.blueprints.get('staff'):
    app.register_blueprint(staff_bp) # المسار معرف داخلياً بـ /admin/staff
    logger.info("👥 تم تفعيل نظام حوكمة الطاقم بنجاح")

def patch_database():
    """تحديث هيكل الجداول ليتوافق مع التعديلات السيادية الجديدة (إصلاح أخطاء Railway)"""
    with app.app_context():
        sql_commands = [
            # --- تحديث جدول المستخدمين (نظام الصلاحيات والتحقق الجديد) ---
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(150);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_login TIMESTAMP;",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS last_ip VARCHAR(45);",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS permissions TEXT DEFAULT '{}';",
            "ALTER TABLE users ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id);",
            
            # --- تحديث جدول الموردين (Suppliers) ---
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS identity_type VARCHAR(50);",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS identity_image_url VARCHAR(255);",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS mint_sovereign_id VARCHAR(100) UNIQUE;",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS tier VARCHAR(50) DEFAULT 'مورد مبتدئ';",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_yer NUMERIC(20, 2) DEFAULT 0.00;",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_sar NUMERIC(20, 2) DEFAULT 0.00;",
            "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_usd NUMERIC(20, 2) DEFAULT 0.00;"
        ]
        
        logger.info("🔍 جاري فحص وتحديث الترسانة الرقمية (Auto-Repair)...")
        for cmd in sql_commands:
            try:
                db.session.execute(text(cmd))
                db.session.commit()
            except Exception as e:
                db.session.rollback()
                logger.debug(f"ℹ️ حقل موجود مسبقاً أو تنبيه بسيط: {str(e)}")
        logger.info("✅ تم تعميد هيكل الجداول بنجاح والقاعدة جاهزة.")

def initialize_system():
    """تهيئة النظام السيادي عند الإقلاع"""
    with app.app_context():
        try:
            # 1. إنشاء الجداول الأساسية
            db.create_all()
            
            # 2. تشغيل جسر الترميم (تحديث الأعمدة)
            patch_database()
            
            # 3. تأمين حساب القائد علي محجوب (Super Admin)
            admin_username = "علي محجوب"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                new_admin = User(
                    username=admin_username, 
                    full_name="المهندس علي محجوب",
                    role='super_admin', # الرتبة الأعلى في النظام
                    permissions='{"all": true}',
                    is_active=True
                )
                new_admin.set_password('123') 
                db.session.add(new_admin)
                db.session.commit()
                logger.info(f"👤 تم إنشاء حساب القائد الأعلى: {admin_username}") 
            else:
                # التأكد من بقاء الرتبة سيادية وتحديث الصلاحيات
                admin.role = 'super_admin'
                db.session.commit()
                logger.info(f"✅ القائد {admin_username} في مركز القيادة السيادي.")
                
        except Exception as e:
            logger.error(f"⚠️ خطأ فادح أثناء التهيئة: {str(e)}")

# بروتوكول التشغيل (يضمن التنفيذ مرة واحدة فقط)
if os.environ.get("WERKZEUG_RUN_MAIN") == "true" or not app.debug:
    initialize_system()

if __name__ == "__main__":
    # تشغيل المنصة على المنفذ المخصص من Railway
    port = int(os.environ.get("PORT", 8080))
    logger.info(f"🚀 انطلاق منصة محجوب أونلاين على المنفذ: {port}")
    app.run(host='0.0.0.0', port=port, debug=True)
