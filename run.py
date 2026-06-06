# coding: utf-8
# 📂 run.py - نسخة الإنتاج ذاتية الإصلاح (Self-Healing & Auto-Seeding)

import os
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser
from sqlalchemy import text

# 1. تهيئة التطبيق
app = create_app()

def auto_repair_db():
    """
    نظام الإصلاح التلقائي: يتم استدعاؤه بعد تهيئة التطبيق بالكامل.
    يضمن وجود الجداول والأعمدة اللازمة، ويقوم بزرع البيانات التمهيدية.
    """
    with app.app_context():
        try:
            # إنشاء الجداول الأساسية
            db.create_all()
            
            # إصلاحات هيكلية آمنة
            queries = [
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS search_name VARCHAR(150);",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS search_phone VARCHAR(20);",
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_sar FLOAT DEFAULT 0;",
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_yer FLOAT DEFAULT 0;",
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS balance_usd FLOAT DEFAULT 0;",
                "ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS currency VARCHAR(10) DEFAULT 'YER';",
                "ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS description TEXT;",
                "ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'completed';"
            ]
            
            for q in queries:
                try:
                    db.session.execute(text(q))
                except Exception:
                    continue
            
            db.session.commit()
            print("✅ نظام الإصلاح الذاتي: تم مزامنة هيكل الجداول بنجاح.")
            
            # التأكد من وجود الهوية السيادية (Admin)
            if not AdminUser.query.filter_by(username="محجوب").first():
                new_admin = AdminUser(username="محجوب", phone_number="0000000000", role='Owner')
                new_admin.set_password("123")
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم التأكد من وجود الهوية السيادية (Admin).")
            
            # نظام الزرع التلقائي (Seed) لمرة واحدة فقط
            # نستخدم ملفاً صغيراً كعلامة (Flag) لمنع إعادة الزرع في كل مرة
            if not os.path.exists("seed_done.txt"):
                print("🌱 بدء عملية زراعة البيانات التلقائية...")
                from db_reset import seed_data
                seed_data()
                with open("seed_done.txt", "w") as f:
                    f.write("seeded")
                print("🏁 اكتملت عملية الزرع التلقائي.")
            
        except Exception as e:
            print(f"🚨 خطأ في نظام الإصلاح التلقائي: {e}")
            db.session.rollback()

if __name__ == "__main__":
    auto_repair_db()
    # تشغيل التطبيق
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
