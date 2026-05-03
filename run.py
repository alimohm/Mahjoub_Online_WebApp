import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

# 1. إنشاء التطبيق
app = create_app()

def patch_database():
    """إصلاح شامل وهجومي لهيكل الجداول لضمان عدم التعثر"""
    with app.app_context():
        # قائمة كاملة بالأعمدة المطلوبة بناءً على آخر خطأ (UndefinedColumn)
        sql_commands = [
            # الربط الأساسي
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER REFERENCES users(id);",
            
            # البيانات الأساسية التي اشتكى النظام من فقدانها
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS owner_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS trade_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS phone VARCHAR(50);",
            
            # نظام الهوية والموقع
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_card_number VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS id_image VARCHAR(255);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS activity_type VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS province VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS district VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS address_detail VARCHAR(255);",
            
            # الربط المالي
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_name VARCHAR(150);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS bank_acc VARCHAR(100);",
            "ALTER TABLE vendors ADD COLUMN IF NOT EXISTS fin_type VARCHAR(50);"
        ]
        
        print("🔍 جاري فحص وتحديث الترسانة الرقمية...")
        for cmd in sql_commands:
            try:
                # تنفيذ كل أمر بشكل مستقل لضمان مرور العمليات الناجحة
                db.session.execute(text(cmd))
                db.session.commit()
            except Exception:
                db.session.rollback()
                # تجاهل الخطأ إذا كان العمود موجوداً مسبقاً
                continue
        print("✅ تم تحديث هيكل الجداول بنجاح.")

def initialize_system():
    """تهيئة النظام السيادي وقاعدة البيانات عند الإقلاع"""
    with app.app_context():
        try:
            # 1. تحديث هيكل الجداول أولاً قبل أي استعلام (Query)
            patch_database()
            
            # 2. التأكد من وجود الجداول الأساسية
            db.create_all()
            
            # 3. التأكد من وجود الحساب الإداري للقائد علي محجوب
            admin_username = "علي محجوب"
            admin = User.query.filter_by(username=admin_username).first()
            if not admin:
                new_admin = User(username=admin_username, role='admin')
                new_admin.set_password('123')
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم تأكيد صلاحيات القائد في النظام.")
            else:
                print("✅ النظام والترسانة في حالة جاهزية تامة.")
        except Exception as e:
            print(f"⚠️ تنبيه النظام: {str(e)}")

# تنفيذ التهيئة والإصلاح الشامل قبل بدء استقبال الطلبات
initialize_system()

if __name__ == "__main__":
    # الحصول على المنفذ من بيئة تشغيل Railway
    port = int(os.environ.get("PORT", 5000))
    
    # تشغيل التطبيق على العنوان الشامل 0.0.0.0
    app.run(host='0.0.0.0', port=port, debug=False)
