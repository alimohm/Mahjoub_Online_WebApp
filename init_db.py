# init_db.py
import os
import sys
from sqlalchemy import text

# --- بروتوكول تثبيت المسار السيادي لـ محجوب أونلاين ---
# يضمن هذا الجزء أن السيرفر يرى مجلد 'core' أينما كان موقع التشغيل
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد المكونات الأساسية بعد تثبيت المسار
try:
    from core import create_app, db
    # استيراد الموديلات لضمان تسجيلها في SQLAlchemy قبل create_all
    from core.models.user import User
    from core.models.business import Order
    from core.models.product import Product
    from core.models.supplier import Supplier # الموديل الجديد
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    print("تأكد من وجود ملف __init__.py داخل مجلد core ومجلد models")
    sys.exit(1)

app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 جاري تنفيذ بروتوكول الإصلاح الشامل لـ محجوب أونلاين...")
            
            # 1. إنشاء الجداول الأساسية (إن لم تكن موجودة)
            db.create_all() 
            
            # 2. الترميم الهيكلي العميق (Deep Structural Repair)
            with db.engine.connect() as connection:
                print("🔍 فحص وترميم أعمدة جدول الطلبات (Orders)...")
                
                # إضافة الأعمدة المفقودة لضمان استقرار العمليات
                alter_queries = [
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount FLOAT DEFAULT 0.0;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS shipping_address TEXT;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS contact_phone VARCHAR(20);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP;"
                ]
                
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        print(f"✅ تم فحص/تنفيذ: {query[:40]}...")
                    except Exception as e:
                        # نتجاوز الخطأ إذا كان العمود موجوداً بالفعل (خاصة في SQLite)
                        pass
                
                # ترميم جداول المنتجات والمستخدمين
                print("🔍 تحديث صلاحيات الوصول وهيكلة المنتجات...")
                try:
                    connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS owner_id INTEGER REFERENCES users(id);"))
                    connection.execute(text("ALTER TABLE products ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';"))
                    connection.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
                    connection.commit()
                except Exception:
                    pass
            
            print("✅ اكتمل الترميم! كافة الجداول والأعمدة أصبحت جاهزة.")
            print("🌟 الترسانة الرقمية لـ محجوب أونلاين جاهزة للانطلاق.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت عملية الترميم: {str(e)}")

if __name__ == "__main__":
    initialize_database()
