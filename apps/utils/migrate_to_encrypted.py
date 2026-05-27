# coding: utf-8
# 🚀 سكربت ترحيل البيانات المشفرة - منصة محجوب أونلاين 2026
from apps import create_app
from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import SupplierWallet, WalletTransaction

def run_migration():
    # 1. إنشاء نسخة من التطبيق لتهيئة البيئة (App Factory)
    app = create_app()
    
    # 2. الدخول في سياق التطبيق للوصول إلى قاعدة البيانات والمشفر
    with app.app_context():
        print("🚀 بدء عملية الترحيل المشفر...")
        
        try:
            # 3. معالجة الموردين
            for s in Supplier.query.all():
                s.owner_name = s.owner_name 
                s.trade_name = s.trade_name
                print(f"✅ تمت معالجة المورد: {s.sovereign_id}")
            
            # 4. معالجة كشوفات الحسابات
            for stmt in SupplierStatement.query.all():
                stmt.description = stmt.description
                stmt.debit = stmt.debit
                stmt.credit = stmt.credit
                stmt.running_balance = stmt.running_balance
            
            # 5. معالجة المحافظ
            for w in SupplierWallet.query.all():
                w.yer_total = w.yer_total
                w.sar_total = w.sar_total
                w.usd_total = w.usd_total
                
            # 6. معالجة الحركات
            for tx in WalletTransaction.query.all():
                tx.amount = tx.amount
                tx.profit_margin = tx.profit_margin
                tx.notes = tx.notes

            # 7. الحفظ النهائي في قاعدة البيانات
            db.session.commit()
            print("🎉 اكتملت عملية الترحيل بنجاح وتم تشفير كافة البيانات!")
            
        except Exception as e:
            db.session.rollback()
            print(f"❌ حدث خطأ أثناء الترحيل: {str(e)}")

if __name__ == "__main__":
    run_migration()
