# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

app = create_app()

def auto_fix_database():
    """هذه الدالة تقوم بفحص الأعمدة المفقودة وإضافتها برمجياً"""
    with app.app_context():
        try:
            print("🔧 جاري فحص هيكل قاعدة البيانات...")
            
            # 1. فحص جدول المحافظ
            inspector = inspect(db.engine)
            columns = [c['name'] for c in inspector.get_columns('supplier_wallets')]
            
            # قائمة الأعمدة التي نتوقع وجودها
            required_columns = ['_yer_total', '_sar_total', '_usd_total']
            
            for col in required_columns:
                if col not in columns:
                    print(f"⚠️ العمود {col} مفقود، جاري إضافته...")
                    db.session.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col} VARCHAR(255)"))
                    db.session.commit()
                    print(f"✅ تم إضافة {col} بنجاح.")
            
            print("🚀 قاعدة البيانات محدثة وجاهزة للعمل.")
            
        except Exception as e:
            print(f"❌ خطأ أثناء التحديث التلقائي: {str(e)}")
            db.session.rollback()

# استدعاء دالة الإصلاح قبل تشغيل التطبيق
auto_fix_database()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
