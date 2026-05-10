# admin_panel/suppliers_logic.py
import random
import string
from core import db
from core.models.supplier import Supplier
from werkzeug.security import generate_password_hash

class SupplierLogic:
    @staticmethod
    def generate_temp_password(length=5):
        """توليد كلمة مرور عشوائية مكونة من أرقام فقط"""
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def register_supplier(form_data):
        """محرك تعميد الموردين: تشفير الهوية وحفظها في الترسانة"""
        try:
            # 1. توليد المعرف السيادي SUP_
            last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
            new_sovereign_id = f"SUP_{last_id + 1}#"

            # 2. إنشاء الهوية المؤقتة (أرقام فقط)
            temp_pass = SupplierLogic.generate_temp_password(5)
            # اسم المستخدم يكون المعرف السيادي أو رقم الهاتف (حسب رغبتك)
            username = form_data.get('username') or f"user_{last_id + 1}"

            # 3. إنشاء الكيان الجديد مع تشفير كلمة المرور
            new_supplier = Supplier(
                sovereign_id=new_sovereign_id,
                username=username,
                password_hash=generate_password_hash(temp_pass), # تشفير سيادي
                trade_name=form_data.get('trade_name'),
                owner_name=form_data.get('owner_name'),
                activity_type=form_data.get('activity_type'),
                identity_type=form_data.get('identity_type'),
                province=form_data.get('province'),
                district=form_data.get('district'),
                address_detail=form_data.get('address_detail'),
                phone=form_data.get('phone'),
                bank_name=form_data.get('bank_name'),
                bank_acc=form_data.get('bank_acc'),
                status='active'
            )

            db.session.add(new_supplier)
            db.session.commit()
            
            # إرجاع كلمة المرور في رسالة النجاح لكي تسلمها للمورد
            return True, f"تم التعميد! اسم المستخدم: {username} | كلمة السر المؤقتة: {temp_pass}"

        except Exception as e:
            db.session.rollback()
            return False, f"فشل في التعميد: {str(e)}"

    @staticmethod
    def get_next_id():
        """توليد المعرف التالي لإظهاره في الواجهة"""
        last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
        return f"SUP_{last_id + 1}#"

    @staticmethod
    def search_suppliers(query=None, status=None):
        """محرك البحث في الرادار السيادي"""
        s_query = Supplier.query
        if query:
            s_query = s_query.filter(
                (Supplier.trade_name.contains(query)) | 
                (Supplier.sovereign_id.contains(query)) |
                (Supplier.username.contains(query))
            )
        if status:
            s_query = s_query.filter_by(status=status)
            
        return s_query.order_by(Supplier.created_at.desc()).all()
