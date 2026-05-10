# admin_panel/engines/supplier_engine.py
from core import db
from core.models.supplier import Supplier

def create_new_supplier(form_data):
    """المحرك المسؤول عن هندسة بيانات المورد الجديد"""
    try:
        # 1. إنشاء الكائن من البيانات الخام
        new_supplier = Supplier(
            username=form_data.get('username'),
            trade_name=form_data.get('trade_name'),
            owner_name=form_data.get('owner_name'),
            activity_type=form_data.get('activity_type'),
            identity_type=form_data.get('identity_type'),
            phone=form_data.get('phone'),
            email=form_data.get('email'),
            bank_name=form_data.get('bank_name'),
            bank_acc=form_data.get('bank_acc'),
            province=form_data.get('province'),
            district=form_data.get('district'),
            address_detail=form_data.get('address_detail')
        )

        # 2. استدعاء وظائف الموديل الذكية (التوليد والتشفير)
        new_supplier.generate_sovereign_codes()
        new_supplier.set_password(form_data.get('password', '123456'))

        # 3. الحفظ في القاعدة
        db.session.add(new_supplier)
        db.session.commit()
        
        return True, new_supplier.sovereign_id
    except Exception as e:
        db.session.rollback()
        return False, str(e)
