# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text, inspect

app = create_app()

def auto_fix_database():
    with app.app_context():
        try:
            print("🔧 جاري إصلاح هيكل قاعدة البيانات تلقائياً...")
            inspector = inspect(db.engine)
            # إضافة الأعمدة المفقودة لجدول المعاملات
            if 'wallet_transactions' in inspector.get_table_names():
                cols = [c['name'] for c in inspector.get_columns('wallet_transactions')]
                for col in ['_amount', '_profit_margin', '_notes']:
                    if col not in cols:
                        db.session.execute(text(f"ALTER TABLE wallet_transactions ADD COLUMN {col} VARCHAR(255)"))
                db.session.commit()
            
            # إضافة الأعمدة المفقودة لجدول المحافظ
            if 'supplier_wallets' in inspector.get_table_names():
                cols = [c['name'] for c in inspector.get_columns('supplier_wallets')]
                for col in ['_yer_total', '_sar_total', '_usd_total']:
                    if col not in cols:
                        db.session.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN {col} VARCHAR(255)"))
                db.session.commit()
            print("✅ تم إصلاح الهيكل بنجاح.")
        except Exception as e:
            print(f"❌ فشل الإصلاح: {e}")
            db.session.rollback()

auto_fix_database()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
