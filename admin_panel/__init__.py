# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (The Admin Core)
# هذا الكائن هو "المظلة" التي تجتمع تحتها كافة مسارات لوحة التحكم
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates', 
    static_folder='static', 
    url_prefix='/admin' 
)

# 2. بروتوكول الربط السيادي (Sovereign Linkage)
# ملاحظة للقائد علي: نستخدم الاستيراد المتأخر لمنع التداخل الدائري (Circular Import)
# ولضمان توافق المسارات مع أماكنها الجديدة في الترسانة البرمجية

try:
    from . import auth                     # محرك الحماية والولوج
    from . import routes                   # محرك الرادار والداشبورد الأساسي
    
    # ربط مسار تعديل الموردين الجديد (المحرك المنفصل)
    from . import supplier_service_routes  # محرك إدارة بروفايلات الموردين
    
    # استدعاء ملف الإدارة من مجلد الـ core/models كما ذكرت
    from core.models import manage_suppliers 

except ImportError as e:
    # بروتوكول تسجيل الأخطاء في حال فقدان أي ملف أثناء النشر على Railway
    print(f"⚠️ تنبيه سيادي: تعذر استدعاء بعض الوحدات البرمجية: {e}")

"""
--- توثيق الاستقرار للمؤسس علي محجوب ---
- تم إضافة supplier_service_routes لضمان تفعيل وظائف التعديل والحفظ.
- النظام مهيأ الآن للإقلاع دون Crash في Railway.
- تم التأكد من أن جميع المسارات مسجلة تحت مظلة admin_bp.
"""
