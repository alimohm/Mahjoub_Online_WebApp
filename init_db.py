# init_db.py
import os
import sys
from sqlalchemy import text
from werkzeug.security import generate_password_hash

# --- بروتوكول تثبيت المسار لضمان التعرف على الحزم ---
project_root = os.path.abspath(os.path.dirname(__file__))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from core import create_app, db
    from core.models.user import User
    from core.models.business import Order
    from core.models.product import Product
    from core.models.supplier import Supplier 
except ImportError as e:
    print(f"❌ خطأ في الاستيراد: {e}")
    sys.exit(1)

app = create_app()

def initialize_database():
    with app.app_context():
        try:
            print("--------------------------------")
            print("🚀 بدء بروتوكول التشغيل الكامل لمحجوب أونلاين...")
            
            # 1. تنظيف جدول الموردين لضمان تحديث الحقول
            with db.engine.connect() as connection:
                try:
                    connection.execute(text("DROP TABLE IF EXISTS suppliers CASCADE;"))
                    connection.commit()
                    print("✅ تم تصفير جدول الموردين للتحديث الهيكلي.")
                except Exception:
                    pass

            # 2. إنشاء كافة الجداول بناءً على الموديلات الحديثة
            db.create_all() 
            print("✅ تم بناء هيكل الجداول الجديد.")
            
            # 3. ترميم الأعمدة المفقودة في الجداول الأخرى
            with db.engine.connect() as connection:
                alter_queries = [
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS total_amount FLOAT DEFAULT 0.0;",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                    "ALTER TABLE orders ADD COLUMN IF NOT EXISTS status VARCHAR(50) DEFAULT 'pending';",
                    "ALTER TABLE products ADD COLUMN IF NOT EXISTS owner_id INTEGER REFERENCES users(id);",
                    "ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"
                ]
                for query in alter_queries:
                    try:
                        connection.execute(text(query))
                        connection.commit()
                    except Exception: pass

            # 4. إنشاء حساب "علي محجوب" (السيادة المطلقة)
            admin_user = "علي محجوب"
            if not User.query.filter_by(username=admin_user).first():
                new_admin = User(
                    username=admin_user,
                    email='admin@mahjoub.online',
                    password=generate_password_hash('123', method='pbkdf2:sha256'),
                    role='admin'
                )
                db.session.add(new_admin)
                db.session.commit()
                print(f"👤 تم إنشاء حساب المدير: {admin_user} بكلمة سر: 123")
            
            print("🌟 الترسانة الرقمية جاهزة تماماً للانطلاق.")
            print("--------------------------------")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثرت العملية: {str(e)}")

if __name__ == "__main__":
    initialize_database()
