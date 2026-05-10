# admin_panel/suppliers_logic.py
import random
import string
from core import db
from core.models.supplier import Supplier
from werkzeug.security import generate_password_hash

class SupplierLogic:
    
    # --- 1. محركات التوليد والتشهير ---
    
    @staticmethod
    def generate_temp_password(length=5):
        """توليد كلمة مرور عشوائية مكونة من أرقام فقط (Security Code)"""
        return ''.join(random.choices(string.digits, k=length))

    @staticmethod
    def get_next_id():
        """استباق المعرف التالي لعرضه في واجهة الإدخال الملكية"""
        last_id = db.session.query(db.func.max(Supplier.id)).scalar() or 0
        return f"SUP_{last_id + 1}#"

    # --- 2. محركات الإدارة والتعميد (Write Operations) ---

    @staticmethod
    def register_supplier(form_data):
        """محرك تعميد الموردين: إنشاء الهوية الرقمية، التشفير، والتثبيت في القاعدة"""
        try:
            # 1. توليد المعرف السيادي
            next_id_int = (db.session.query(db.func.max(Supplier.id)).scalar() or 0) + 1
            new_sovereign_id = f"SUP_{next_id_int}#"

            # 2. إنشاء بيانات الدخول
            temp_pass = SupplierLogic.generate_temp_password(5)
            username = form_data.get('username') or f"m_user_{next_id_int}"

            # 3. إنشاء الكيان الجديد
            new_supplier = Supplier(
                sovereign_id=new_sovereign_id,
                username=username,
                password_hash=generate_password_hash(temp_pass),
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
                status='active',
                tier=form_data.get('tier', 'مبتدئ')
            )

            db.session.add(new_supplier)
            db.session.commit()
            
            return True, f"تم التعميد بنجاح! اسم المستخدم: {username} | كلمة المرور: {temp_pass}"

        except Exception as e:
            db.session.rollback()
            return False, f"تعثر بروتوكول التعميد: {str(e)}"

    @staticmethod
    def update_supplier_data(s_id, data):
        """تحديث بيانات الكيان والأرصدة السيادية"""
        try:
            supplier = Supplier.query.get(s_id)
            if not supplier:
                return False, "الكيان غير موجود في الأرشيف"
            
            # تحديث الحقول الأساسية إذا وجدت في الطلب
            for field in ['trade_name', 'status', 'tier', 'province', 'phone']:
                if field in data:
                    setattr(supplier, field, data[field])
            
            # تحديث الأرصدة (إذا تم تمريرها)
            if 'balance_yer' in data: supplier.balance_yer = data['balance_yer']
            if 'balance_sar' in data: supplier.balance_sar = data['balance_sar']
            if 'balance_usd' in data: supplier.balance_usd = data['balance_usd']

            db.session.commit()
            return True, "تم تحديث الترسانة بنجاح"
        except Exception as e:
            db.session.rollback()
            return False, f"فشل التحديث: {str(e)}"

    @staticmethod
    def delete_entity(s_id):
        """حذف الكيان من القاعدة (إجراء سيادي نهائي)"""
        try:
            supplier = Supplier.query.get(s_id)
            if supplier:
                db.session.delete(supplier)
                db.session.commit()
                return True, "تم مسح الكيان نهائياً"
            return False, "الكيان غير موجود بالفعل"
        except Exception as e:
            db.session.rollback()
            return False, f"فشل الحذف: {str(e)}"

    # --- 3. محركات الرصد والاستعلام (Read Operations) ---

    @staticmethod
    def search_suppliers(query=None, filters=None):
        """محرك رادار الموردين المتقدم: البحث، الفرز، والفلترة"""
        s_query = Supplier.query
        
        # البحث النصي الشامل
        if query and query != "#":
            search_pattern = f"%{query}%"
            s_query = s_query.filter(
                db.or_(
                    Supplier.trade_name.like(search_pattern),
                    Supplier.sovereign_id.like(search_pattern),
                    Supplier.username.like(search_pattern),
                    Supplier.phone.like(search_pattern)
                )
            )
        
        # تطبيق الفلاتر الإضافية
        if filters:
            if filters.get('province'):
                s_query = s_query.filter(Supplier.province == filters['province'])
            if filters.get('status'):
                s_query = s_query.filter(Supplier.status == filters['status'])
            if filters.get('tier'):
                s_query = s_query.filter(Supplier.tier == filters['tier'])
            
        return s_query.order_by(Supplier.id.desc()).all()

    @staticmethod
    def get_full_details(s_id):
        """جلب البصمة الرقمية الكاملة للمورد"""
        supplier = Supplier.query.get(s_id)
        if supplier:
            # استخدام to_dict إذا كانت معرفة في الموديل، أو بناؤها يدوياً
            if hasattr(supplier, 'to_dict'):
                return supplier.to_dict()
            return {
                "id": supplier.id,
                "sovereign_id": supplier.sovereign_id,
                "trade_name": supplier.trade_name,
                "owner_name": supplier.owner_name,
                "phone": supplier.phone,
                "province": supplier.province,
                "status": supplier.status,
                "balance_yer": float(supplier.balance_yer or 0),
                "balance_sar": float(supplier.balance_sar or 0),
                "balance_usd": float(supplier.balance_usd or 0)
            }
        return None
