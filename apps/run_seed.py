# 📂 apps/run_seed.py
import os
from apps.extensions import db
from apps.models.admin_db import AdminUser
from sqlalchemy import text

def auto_repair_db():
    """
    نظام الإصلاح التلقائي: يتم استدعاؤه داخل المصنع (factory) عند تشغيل التطبيق.
    يضمن جهوزية الجداول، إضافة الأعمدة الناقصة، إنشاء مدير النظام، 
    وزرع البيانات الأساسية لمرة واحدة فقط.
    """
    try:
        # 1. إنشاء الجداول في حال عدم وجودها
        db.create_all()
        
        # 2. إصلاحات هيكلية (إضافة أعمدة مفقودة في حال حدوث تحديثات لاحقة)
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
        
        # 3. التأكد من وجود المسؤول (محجوب)
        if not AdminUser.query.filter_by(username="محجوب").first():
            new_admin = AdminUser(username="محجوب", phone_number="0000000000", role='Owner')
            new_admin.set_password("123")
            db.session.add(new_admin)
            db.session.commit()
            print("✅ تم التأكد من وجود الهوية السيادية (Admin).")
        
        # 4. نظام الزرع التلقائي (Seed) لمرة واحدة فقط
        # نستخدم ملفاً كعلامة لمنع التكرار في كل مرة يُعاد فيها تشغيل السيرفر
        seed_flag = "seed_done.txt"
        if not os.path.exists(seed_flag):
            print("🌱 بدء عملية زراعة البيانات التلقائية...")
            try:
                # استدعاء ملف الزرع الخارجي الذي يحتوي على البيانات الفعلية
                from db_reset import seed_data
                seed_data()
                
                # إنشاء الملف كعلامة نجاح
                with open(seed_flag, "w") as f:
                    f.write("seeded")
                print("🏁 اكتملت عملية الزرع التلقائي بنجاح.")
            except ImportError:
                print("⚠️ تحذير: لم يتم العثور على ملف db_reset.py في المجلد الجذر.")
            except Exception as e:
                print(f"🚨 خطأ أثناء تنفيذ الزرع: {e}")
        else:
            print("ℹ️ نظام الزرع: البيانات تم زرعها مسبقاً.")
            
    except Exception as e:
        print(f"🚨 خطأ جسيم في نظام الإصلاح التلقائي: {e}")
        db.session.rollback()
