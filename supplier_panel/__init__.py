from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) الخاص بالموردين
# تم تحديد template_folder ليكون 'templates' ليتوافق مع المسار:
# supplier_panel/templates/supplier_panel/filename.html
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. ربط المكونات الداخلية للبوابة
# ملاحظة: الاستيراد يتم في الأسفل لتجنب خطأ "الاستيراد الدائري" (Circular Import)
# لضمان أن كائن supplier_bp قد تم تعريفه أولاً قبل أن تطلبه الملفات الأخرى
try:
    from . import routes
    from . import auth_logic
    from . import decorators
    
    print("🚀 [System] تم تفعيل ترسانة الموردين بنجاح.")
    
except ImportError as e:
    # في حال وجود خطأ في أي ملف داخلي، سيظهر التنبيه في سجلات Railway
    print(f"⚠️ [Critical Error] فشل في ربط مكونات بوابة الموردين: {e}")

# تصدير الكائن ليكون متاحاً للاستدعاء من قبل ملف core/__init__.py
__all__ = ['supplier_bp']
