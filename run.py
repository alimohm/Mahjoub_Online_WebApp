# coding: utf-8
from apps import create_app
from apps.extensions import db
from sqlalchemy import text
import os

# إنشاء التطبيق
app = create_app()

# دالة الترميم التلقائي
def repair_database():
    with app.app_context():
        try:
            print("🚀 جاري محاولة ترميم قاعدة البيانات...")
            # تنفيذ أوامر إضافة الأعمدة برمجياً
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _amount VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _profit_margin VARCHAR(255)"))
            db.session.execute(text("ALTER TABLE wallet_transactions ADD COLUMN IF NOT EXISTS _notes TEXT"))
            db.session.commit()
            print("✅ تم ترميم الأعمدة بنجاح.")
        except Exception as e:
            print(f"⚠️ فشل الترميم (ربما الأعمدة موجودة مسبقاً): {e}")
            db.session.rollback()

# تشغيل وظيفة الترميم قبل بدء التطبيق
repair_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
