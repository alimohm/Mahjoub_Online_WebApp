# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text

# إنشاء التطبيق
app = create_app()

def run_db_migrations():
    """دالة واحدة شاملة لتحديث هيكل قاعدة البيانات عند الإقلاع"""
    with app.app_context():
        try:
            print("🔧 جاري التحقق من تحديثات قاعدة البيانات...")
            
            # أوامر التحديث (ALTER TABLE)
            commands = [
                # تحديث الموردين
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS category VARCHAR(50) DEFAULT 'عام'",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS behavior_score FLOAT DEFAULT 100.0",
                "ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS total_transactions INTEGER DEFAULT 0",
                # تحديث المحافظ
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _yer_total VARCHAR(255) DEFAULT '0.00'",
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _sar_total VARCHAR(255) DEFAULT '0.00'",
                "ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS _usd_total VARCHAR(255) DEFAULT '0.00'"
            ]
            
            for cmd in commands:
                db.session.execute(text(cmd))
            
            db.session.commit()
            print("✅ تم تحديث هيكل قاعدة البيانات بنجاح.")
        except Exception as e:
            print(f"⚠️ خطأ أثناء تحديث القاعدة: {e}")
            db.session.rollback()

# تشغيل الفحص قبل بدء السيرفر
run_db_migrations()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
