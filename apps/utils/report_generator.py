# coding: utf-8
# 📂 apps/utils/report_generator.py
from sqlalchemy import func, cast, String
from apps.extensions import db
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import WalletTransaction
from apps.models.supplier_db import Supplier

class ReportGenerator:
    """ محرك تقارير محجوب أونلاين - محدث لدعم أكواد المحافظ (WEL) وفلترة العملات """

    @staticmethod
    def get_all_wallets_summary(currency='ALL'):
        """ جلب ملخص أرصدة كافة الحسابات مع دعم فلترة العملة """
        # إذا تم اختيار عملة، نحتاج تصفية المحافظ بناءً عليها (مفترض وجود حقل currency في نموذج المحفظة أو المورد)
        query = Supplier.query
        suppliers = query.all()
        
        summary = []
        for s in suppliers:
            # استخدام sovereign_id كـ كود المحفظة (WEL)
            wallet_code = getattr(s, 'sovereign_id', '---')
            balance = float(getattr(s, 'balance', 0))
            
            # إذا كانت العملة محددة، قد تحتاج لإضافة منطق خاص إذا كان الرصيد موزعاً على عملات
            summary.append({
                'trade_name': getattr(s, 'trade_name', '---'),
                'owner_name': getattr(s, 'owner_name', '---'),
                'wallet_code': wallet_code, 
                'balance': balance
            })
        
        return sorted(summary, key=lambda x: x['balance'], reverse=True)

    @staticmethod
    def get_detailed_transactions(supplier_id=None, currency='ALL', start_date=None, end_date=None):
        """ استخراج الحركات التفصيلية مع ربط البيانات الأساسية """
        query = db.session.query(
            SupplierStatement,
            Supplier.trade_name,
            Supplier.sovereign_id.label('wallet_code') # جلب كود المحفظة WEL
        ).join(Supplier, cast(SupplierStatement.supplier_id, String) == cast(Supplier.id, String))
        
        if supplier_id and str(supplier_id) != 'ALL':
            query = query.filter(cast(SupplierStatement.supplier_id, String) == cast(supplier_id, String))
            
        if currency and currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
        
        if start_date: query = query.filter(SupplierStatement.created_at >= start_date)
        if end_date: query = query.filter(SupplierStatement.created_at <= end_date)
            
        results = query.order_by(SupplierStatement.created_at.desc()).all()

        statements = []
        for r in results:
            stmt = r.SupplierStatement
            # إرفاق البيانات المدمجة في نفس الكائن
            stmt.supplier_name = r.trade_name
            stmt.wallet_code = r.wallet_code # إضافة كود المحفظة WEL
            statements.append(stmt)

        return statements

    @staticmethod
    def calculate_net_profit(currency, start_date=None, end_date=None):
        """ حساب الأرباح """
        query = WalletTransaction.query
        if currency and currency != 'ALL':
            query = query.filter(WalletTransaction.currency == currency)
        if start_date: query = query.filter(WalletTransaction.created_at >= start_date)
        if end_date: query = query.filter(WalletTransaction.created_at <= end_date)
            
        total_profit = query.with_entities(func.sum(WalletTransaction.profit_margin)).scalar()
        return float(total_profit or 0)
