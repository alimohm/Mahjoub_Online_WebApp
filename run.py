# coding: utf-8
# 🚀 ملف التشغيل الرئيسي للنواة - محجوب أونلاين 2026
import os
import sys
from apps import create_app
from apps.extensions import db
from sqlalchemy import text

# إنشاء التطبيق
app = create_app()

def apply_database_fixes():
    """وظيفة الإصلاح التلقائي لهيكل قاعدة البيانات عند التشغيل لضمان توافق الجدول مع الموديلات"""
    try:
        with app.app_context():
            print("🔄 جاري التحقق من سلامة هيكل قاعدة البيانات...")
            
            # 1. الأعمدة الناقصة في جدول الموردين (Suppliers)
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'عام'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS behavior_score FLOAT DEFAULT 100.0"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS total_transactions INTEGER DEFAULT 0"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS status VARCHAR(20) DEFAULT 'pending'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS rank_grade VARCHAR(20) DEFAULT 'ريادي'"))
            db.session.execute(text("ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS registration_source VARCHAR(30) DEFAULT 'الموقع الخارجي'"))
            
            # 2. الأعمدة الناقصة في جدول المحافظ (Supplier Wallets) مع قيم افتراضية آمنة
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _yer_total VARCHAR(255) DEFAULT '0.00'"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _sar_total VARCHAR(255) DEFAULT '0.00'"))
            db.session.execute(text("ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _usd_total VARCHAR(255) DEFAULT '0.00'"))
            
            db.session.commit()
            print("✅ تم التأكد من سلامة هيكل قاعدة البيانات بنجاح.")
    except Exception as e:
        print(f"⚠️ تحذير: فشل الإصلاح التلقائي للقاعدة (قد تكون بالفعل محدثة): {e}")
        db.session.rollback()

# فحص أمني: التأكد من وجود مفتاح التشفير
if not app.config.get('ENCRYPTION_KEY') and not os.environ.get('ENCRYPTION_KEY'):
    print("❌ خطأ حرج: ENCRYPTION_KEY غير موجود في متغيرات البيئة!")
    sys.exit(1)

# تطبيق الإصلاحات قبل بدء السيرفر لضمان عمل الدوشبورد
apply_database_fixes()

print("✅ المصنع المركزي للنواة يعمل بنجاح!")
print("🛡️ نظام التشفير (AES-256) مفعل وجاهز.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
