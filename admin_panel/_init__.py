from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) الخاص بلوحة الإدارة
# تم تحديد template_folder لضمان قراءة القوالب من المجلد المنظم:
# admin_panel/templates/admin_panel/
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (Routes)
# يتم الاستيراد هنا في الأسفل لكسر حلقة الاستيراد الدائري (Circular Import)
# لضمان أن كائن admin_bp قد تم تعريفه قبل أن يطلبه ملف routes
try:
    from . import routes
    print("🏰 [System] تم تعميد بوابة الإدارة بنجاح.")
except ImportError as e:
    # سيظهر هذا التنبيه في Railway إذا كان هناك خطأ في ملف routes.py
    print(f"⚠️ [Error] فشل في تحميل مسارات الإدارة: {e}")

# تصدير الكائن ليكون متاحاً للاستدعاء من ملف core/__init__.py
__all__ = ['admin_bp']
