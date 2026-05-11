# admin_panel/engines/supplier_engine.py
from core.extensions import db
from core.models.supplier import Supplier
from sqlalchemy import or_

def create_new_supplier(form_data):
    """المحرك السيادي - نسخة استئصال الأخطاء v4.5"""
    try:
        # 1. طباعة البيانات المستلمة في الـ Logs لمراقبة ما يحدث (اختياري)
        print(f"📡 استلام بيانات المورد: {form_data.get('trade_name')}")

        # 2. إنشاء الكيان مع حماية الحقول (تجنب الحقول التي قد تسبب انهياراً)
        new_supplier = Supplier(
            username=form_data.get('username') or f"user_{form_data.get('phone')}",
            trade_name=form_data.get('trade_name'),
            owner_name=form_data.get('owner_name'),
            phone=form_data.get('phone'),
            province=form_data.get('province'),
            # تجاهل الصورة والملفات حالياً للتأكد من نجاح حفظ النصوص
            status='نشط',
            tier='مبتدئ'
        )

        # 3. محاولة توليد الكود السيادي يدوياً إذا فشلت الدالة التلقائية
        try:
            if hasattr(new_supplier, 'generate_sovereign_codes'):
                new_supplier.generate_sovereign_codes()
            else:
                import uuid
                new_supplier.sovereign_id = f"MAH-{uuid.uuid4().hex[:8].upper()}"
        except Exception as e:
            print(f"⚠️ فشل توليد الكود: {e}")
            new_supplier.sovereign_id = "TEMP-ID"

        # 4. الحفظ النهائي
        db.session.add(new_supplier)
        db.session.commit()
        
        return True, new_supplier.sovereign_id

    except Exception as e:
        db.session.rollback()
        error_msg = str(e)
        print(f"❌ خطأ فادح في المحرك: {error_msg}")
        
        # إذا كان الخطأ متعلقاً بعمود مفقود، سنعرفه هنا
        if "column" in error_msg.lower():
            return False, f"نقص في أعمدة قاعدة البيانات: {error_msg}"
            
        return False, f"انهيار داخلي: {error_msg}"

# لا تنسَ إبقاء دالة get_suppliers_by_filter كما هي أسفل الملف
