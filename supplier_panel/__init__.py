from flask import Blueprint

# تعريف البلوبرنت الخاص بالموردين
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد الروابط والمنطق الداخلي (auth_logic, decorators) في الأسفل
try:
    from . import routes
    from . import auth_logic
    from . import decorators
    print("🚀 [System] بوابة الموردين جاهزة للعمل.")
except ImportError as e:
    print(f"⚠️ [Error] فشل في تحميل مكونات بوابة الموردين: {e}")

# تصدير الكائن ليكون متاحاً للنواة
__all__ = ['supplier_bp']
