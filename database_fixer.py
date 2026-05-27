from sqlalchemy import text
from apps.extensions import db

def apply_database_fixes(app):
    with app.app_context():
        # قائمة بالأعمدة الناقصة في جدول suppliers
        supplier_cols = [
            ("category", "VARCHAR(50) DEFAULT 'عام'"),
            ("behavior_score", "FLOAT DEFAULT 100.0"),
            ("total_transactions", "INTEGER DEFAULT 0"),
            ("status", "VARCHAR(20) DEFAULT 'pending'"),
            ("rank_grade", "VARCHAR(20) DEFAULT 'ريادي'"),
            ("registration_source", "VARCHAR(30) DEFAULT 'الموقع الخارجي'")
        ]
        
        # قائمة بالأعمدة الناقصة في جدول supplier_wallets
        wallet_cols = [
            ("_yer_total", "VARCHAR(255)"),
            ("_sar_total", "VARCHAR(255)"),
            ("_usd_total", "VARCHAR(255)")
        ]

        # تنفيذ الإضافات لجدول الموردين
        for col, col_type in supplier_cols:
            db.session.execute(text(f"ALTER TABLE suppliers ADD COLUMN IF NOT EXISTS {col} {col_type}"))
        
        # تنفيذ الإضافات لجدول المحافظ
        for col, col_type in wallet_cols:
            db.session.execute(text(f"ALTER TABLE supplier_wallets ADD COLUMN IF NOT EXISTS {col} {col_type}"))
            
        db.session.commit()
        print("✅ تم تحديث هيكل قاعدة البيانات تلقائياً.")
