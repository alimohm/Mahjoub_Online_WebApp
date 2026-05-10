# admin_panel/suppliers_logic.py
from core.extensions import db
from core.models.supplier import Supplier
from sqlalchemy import or_

class SupplierLogic:
    @staticmethod
    def approve_supplier(sup_id):
        """منطق التعميد ومنح الهوية الرقمية"""
        supplier = Supplier.query.get(sup_id)
        if not supplier:
            return False, "المورد غير موجود"
        try:
            supplier.status = 'active'
            supplier.mint_sovereign_id() 
            db.session.commit()
            return True, f"تم تعميد الكيان {supplier.trade_name} بنجاح"
        except Exception as e:
            db.session.rollback()
            return False, str(e)

    @staticmethod
    def search_suppliers(query, status):
        """منطق البحث المتقدم"""
        search_filter = Supplier.query
        if query:
            search_filter = search_filter.filter(or_(
                Supplier.trade_name.icontains(query),
                Supplier.owner_name.icontains(query),
                Supplier.sovereign_id.icontains(query)
            ))
        if status:
            search_filter = search_filter.filter(Supplier.status == status)
        return search_filter.order_by(Supplier.id.desc()).all()

    @staticmethod
    def update_supplier_data(sup_id, data):
        """منطق تحديث البيانات والأرصدة"""
        supplier = Supplier.query.get_or_404(sup_id)
        try:
            supplier.owner_name = data.get('owner_name')
            supplier.trade_name = data.get('trade_name')
            supplier.balance_yer = data.get('balance_yer', 0)
            # ... بقية الحقول ...
            if data.get('new_password'):
                supplier.set_password(data.get('new_password'))
            db.session.commit()
            return True, "نجاح"
        except Exception as e:
            db.session.rollback()
            return False, str(e)
