from core import db
from datetime import datetime

class SupplierLogic:
    """
    محرك العمليات السيادي - موديول الموردين
    """

    @staticmethod
    def approve_supplier(sup_id):
        """تعميد المورد وتحويل حالته لنشط"""
        from core.models.supplier import Supplier
        try:
            supplier = Supplier.query.get(sup_id)
            if supplier:
                supplier.status = 'active'
                db.session.commit()
                return True, "تم تعميد المورد بنجاح"
            return False, "المورد غير موجود"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def search_suppliers(query, status_filter):
        """البحث اللحظي في قاعدة بيانات الموردين"""
        from core.models.supplier import Supplier
        try:
            q = Supplier.query
            if query:
                q = q.filter(Supplier.trade_name.contains(query))
            if status_filter:
                q = q.filter(Supplier.status == status_filter)
            return q.all()
        except:
            return []

    @staticmethod
    def get_next_id():
        """حساب المعرف القادم SUP_#"""
        from core.models.supplier import Supplier
        last = Supplier.query.order_by(Supplier.id.desc()).first()
        return f"SUP_{last.id + 1}#" if last else "SUP_1#"
