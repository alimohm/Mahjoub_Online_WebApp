# --- الترسانة السيادية: بوابة شركاء النجاح (الموردين) ---
# الموقع: supplier_panel/__init__.py

from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) الخاص بقطاع الموردين
# تم تحديد 'templates' و 'static' لضمان استدعاء التصميمات الخاصة بالموردين
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. ربط المكونات الوظيفية بالبلوبرنت
# يتم الاستيراد في الأسفل لتجنب خطأ "الاستيراد الدائري" (Circular Import)
try:
    from . import routes
    from . import auth_logic
    from . import decorators
    
    # رسالة فنية تظهر في سجلات السيرفر (Railway/Render) لتأكيد النجاح
    print("🚀 [System] تم تفعيل بوابة الموردين (Supplier Panel) بنجاح.")
    
except ImportError as e:
    print(f"⚠️ [Critical Error] فشل في تحميل مكونات بوابة الموردين: {e}")

# ملاحظة للقائد علي: 
# تأكد أن مجلد supplier_panel يحتوي على مجلد داخلي باسم templates
# لضمان عمل render_template('dashboard.html') بشكل صحيح.
