# core/services/supplier_service.py
from core import db
from core.models.supplier import Supplier
import logging

# إعداد السجلات لمراقبة العمليات السيادية
logger = logging.getLogger(__name__)

def get_all_suppliers():
    """ جلب كافة الموردين مع إحصائياتهم للوحة التحكم """
    try:
        suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
        stats = {
            'total': len(suppliers),
            'active': Supplier.query.filter_by(status='active').count(),
            'sovereign': Supplier.query.filter_by(tier='سيادي').count(),
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0
        }
        return {'suppliers': suppliers, 'stats': stats}
    except Exception as e:
        logger.error(f"⚠️ خطأ في استرجاع قائمة الموردين: {str(e)}")
        return {'suppliers': [], 'stats': {'total': 0, 'active': 0, 'sovereign': 0, 'total_yer': 0}}

def create_supplier(data):
    """ محرك تعميد الموردين الجدد """
    try:
        new_supplier = Supplier(
            username=data.get('username'),
            trade_name=data.get('trade_name'),
            owner_name=data.get('owner_name'),
            activity_type=data.get('activity_type'),
            identity_type=data.get('identity_type'),
            phone=data.get('phone'),
            email=data.get('email'),
            province=data.get('province'),
            district=data.get('district'),
            status='active',
            tier=data.get('tier', 'مبتدئ')
        )
        password = data.get('password') or '123456'
        new_supplier.set_password(password)
        
        # استخدام الدالة المعتمدة في الموديل
        new_supplier.generate_sovereign_codes()
        
        db.session.add(new_supplier)
        db.session.commit()
        logger.info(f"✅ تم تعميد كيان جديد: {new_supplier.trade_name}")
        return True, new_supplier.trade_name
    except Exception as e:
        db.session.rollback()
        return False, str(e)

def update_supplier_profile(supplier_id, data):
    """ بروتوكول تحديث بيانات الكيان مع نظام تتبع (Debug) """
    try:
        logger.info(f"🔍 محاولة تحديث المورد {supplier_id}. البيانات: {data}")
        supplier = Supplier.query.get(supplier_id)
        if not supplier:
            return False, "الكيان غير موجود"

        # تحديث الحقول الأساسية
        supplier.trade_name = data.get('trade_name', supplier.trade_name)
        supplier.owner_name = data.get('owner_name', supplier.owner_name)
        supplier.email = data.get('email', supplier.email)
        supplier.phone = data.get('phone', supplier.phone)
        
        # تحديث الموقع
        supplier.province = data.get('province', supplier.province)
        supplier.district = data.get('district', supplier.district)

        db.session.commit()
        logger.info(f"✅ تم الحفظ بنجاح للكيان: {supplier.trade_name}")
        return True, "تم الحفظ بنجاح"
    except Exception as e:
        db.session.rollback()
        logger.error(f"⚠️ فشل التحديث: {str(e)}")
        return False, str(e)

def get_next_supplier_id():
    """ حساب الرقم التسلسلي القادم """
    try:
        last_sup = Supplier.query.order_by(Supplier.id.desc()).first()
        return (last_sup.id + 1) if last_sup else 1
    except Exception:
        return 1
