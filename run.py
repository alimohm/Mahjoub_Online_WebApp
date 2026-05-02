import os
from sqlalchemy import text
from core import create_app, db
from core.models.user import User

app = create_app()

def build_fortress():
    """بناء قاعدة البيانات وتجهيز الحسابات السيادية"""
    with app.app_context():
        try:
            print("⏳ جاري تهيئة الترسانة الرقمية...")
            # خطوة اختيارية: مسح الجداول القديمة إذا أردت تحديث الهيكل بالكامل
            # db.session.execute(text('DROP TABLE IF EXISTS "user" CASCADE;'))
            
            # إنشاء الجداول فوراً
            db.create_all()
            db.session.commit()
            print("✅ تم بناء الجداول بنجاح.")

            # الآن نتحقق من وجود القائد بعد التأكد من وجود الجدول
            admin_username = "علي محجوب"
            admin_user = User.query.filter_by(username=admin_username).first()
            
            if not admin_user:
                print(f"⚠️ لم يتم العثور على القائد، جاري تنصيب {admin_username}...")
                new_admin = User(username=admin_username, role='admin')
                new_admin.set_password('123') # تذكر تغييرها لاحقاً
                db.session.add(new_admin)
                db.session.commit()
                print(f"👑 تم تنصيب {admin_username} قائداً للمنصة.")
            else:
                print(f"🫡 القائد {admin_username} موجود مسبقاً في برج الرقابة.")

        except Exception as e:
            db.session.rollback()
            print(f"❌ تعثر البناء بسبب: {str(e)}")

# تنفيذ عملية البناء عند التشغيل
build_fortress()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    # نستخدم debug=False في Railway لضمان استقرار العمال (Workers)
    app.run(host='0.0.0.0', port=port, debug=False)
