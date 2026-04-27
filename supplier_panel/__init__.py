from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) مع تحديد مسار فرعي
# إضافة url_prefix='/supplier' تضمن أن روابط الموردين معزولة تماماً عن الإدارة
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    url_prefix='/supplier'  # 👈 هذا السطر يحل مشكلة تداخل المسارات
)

# 2. ربط المكونات (🚨 ضمان تسجيل الروابط والحماية)
try:
    # الاستيراد داخل البلوبرنت يمنع التداخل البرمجي (Circular Import)
    from . import routes 
    from . import auth_logic
    from . import decorators
    
    print("🚀 [System] تم تفعيل بوابة الموردين (المسار: /supplier) بنجاح.")
    
except ImportError as e:
    print(f"⚠️ [Critical Error] فشل في ربط مكونات بوابة الموردين: {e}")

# تصدير الكائن ليكون متاحاً للنواة المركزية في core/__init__.py
__all__ = ['supplier_bp']
