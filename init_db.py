import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- 1. بروتوكول تثبيت المسار (Railway Infrastructure) ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
    from core.models.supplier import Supplier, SupplierStaff
    try:
        from core.models.business import Order
        from core.models.product import Product
    except ImportError:
        Order = None
        Product = None
except ImportError as e:
    print(f"❌ تعذر العثور على النواة (Core Models): {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    """
    بروتوكول تهيئة الترسانة الرقمية المستقرة - منصة محجوب أونلاين v3.7
    تم إضافة حقول full_name و phone لإصلاح أخطاء Postgres في Railway.
    """
    with app.app_context():
        try:
            print("\n" + "="*60)
            print("🚀 بدء بروتوكول التحديث والتعميد - محجوب أونلاين")
            print("="*60)
            
            # 1. بناء الهياكل الجديدة
            db.create_all() 
            print("✅ تم فحص وبناء الهياكل الجديدة (Tables Verified).")
            
            # 2. ترميم الأعمدة المفقودة (إصلاح خطأ column users.full_name does not exist)
            with db.engine.connect() as connection:
                alter_queries = [
                    # حقول جدول المستخدمين (المطلوبة في السجلات)
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS full_name VARCHAR(150);",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS phone VARCHAR(20);",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE;",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS supplier_id INTEGER REFERENCES suppliers(id);",
                    
                    # حقول جدول الموردين السيادية
                    "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS tier VARCHAR(50) DEFAULT 'مبتدئ';",
                    "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS mint_sovereign_id VARCHAR(100) UNIQUE;",
                    "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0.0;",
                    "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0.0;"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: 
                        pass # يتخطى إذا كان العمود موجوداً بالفعل
            print("✅ تم ترميم الأعمدة المفقودة وتحديث الخزينة (Fix Applied).")

            # 3. تأمين حساب المؤسس "علي محجوب"
            admin_user = User.query.filter_by(username="علي محجوب").first()
            if not admin_user:
                new_admin = User(
                    username="علي محجوب",
                    full_name="المهندس علي محجوب", # إضافة الاسم الكامل هنا
                    email='admin@mahjoub.online',
                    role='admin'
                )
                new_admin.set_password('123')
                db.session.add(new_admin)
                print("👤 تم إنشاء حساب المؤسس السيادي (علي محجوب) بنجاح.")
            else:
                # تحديث البيانات إذا كان الحساب موجوداً
                admin_user.role = 'admin'
                if not admin_user.full_name:
                    admin_user.full_name = "المهندس علي محجوب"
                print("ℹ️ حساب المؤسس موجود مسبقاً وتَم تحديث بياناته.")

            db.session.commit()
            print("\n🌟 النظام مستقر الآن، وتم استئصال أخطاء Postgres.")
            print("="*60 + "\n")
            
        except Exception as e:
            db.session.rollback()
            print(f"\n❌ تعثر البروتوكول بسبب: {str(e)}")

if __name__ == "__main__":
    initialize_database()
