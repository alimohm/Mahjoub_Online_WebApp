# coding: utf-8
# 📂 apps/utils/report_generator.py

from apps.extensions import db
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from sqlalchemy import func, and_

class ReportGenerator:

    @staticmethod
    def get_detailed_transactions(supplier_id, currency, start_date, end_date):
        """جلب كشف الحساب التفصيلي مع الفلترة الديناميكية"""
        query = db.session.query(SupplierStatement)
        
        if supplier_id != 'ALL':
            query = query.filter(SupplierStatement.supplier_id == supplier_id)
            
        if currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
            
        if start_date:
            query = query.filter(SupplierStatement.created_at >= start_date)
            
        if end_date:
            query = query.filter(SupplierStatement.created_at <= end_date)
            
        return query.order_by(SupplierStatement.created_at.asc()).all()

    @staticmethod
    def get_all_wallets_summary(currency):
        """جلب ملخص أرصدة جميع الموردين بكفاءة عالية"""
        # استخدام استعلام فرعي لجلب آخر حركة لكل مورد
        subq = db.session.query(
            SupplierStatement.supplier_id,
            func.max(SupplierStatement.created_at).label('max_date')
        ).group_by(SupplierStatement.supplier_id).subquery()

        # دمج النتائج للحصول على الرصيد النهائي لكل مورد
        query = db.session.query(Supplier, SupplierStatement.running_balance).join(
            subq, Supplier.id == subq.c.supplier_id
        ).join(
            SupplierStatement, and_(
                SupplierStatement.supplier_id == subq.c.supplier_id,
                SupplierStatement.created_at == subq.c.max_date
            )
        )

        if currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
            
        data = query.all()
        
        return [{
            'trade_name': getattr(s[0], 'trade_name', '---'),
            'owner_name': getattr(s[0], 'owner_name', '---'),
            'wallet_code': getattr(s[0], 'wallet_code', '---'), # أو sovereign_id حسب المودل
            'balance': float(s[1])
        } for s in data]

    @staticmethod
    def calculate_net_profit(currency, start_date, end_date):
        """حساب إجمالي الأرباح في الفترة المحددة"""
        query = db.session.query(func.sum(SupplierStatement.profit))
        
        if currency != 'ALL':
            query = query.filter(SupplierStatement.currency == currency)
        
        if start_date:
            query = query.filter(SupplierStatement.created_at >= start_date)
            
        if end_date:
            query = query.filter(SupplierStatement.created_at <= end_date)
            
        result = query.scalar()
        return float(result) if result else 0.0
