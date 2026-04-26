from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) السيادي لمجتمع شركاء النجاح
# تم ضبط template_folder ليكون 'templates' ليعرف Flask أين يبحث عن الأرجواني الملكي
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    url_prefix='/supplier' # تأمين المسار تحت بادئة المورد لضمان الاستقرار
)

# 2. ربط المكونات الحيوية بالبلوبرنت
# الاستيراد هنا يأتي بعد تعريف supplier_bp لضمان وصول ملفات الـ routes إليه
try:
    from . import routes
    from . import auth_logic
    from . import decorators
    # سنضيف هنا ملف الـ API مستقبلاً للربط مع قمرة
    # from . import qmr_logic 
except ImportError as e:
    print(f"⚠️ [Critical] فشل في تحميل أحد مكونات الترسانة: {e}")

# 🛡️ رسالة تشغيل في الـ Terminal للتأكد من التحميل عند إقلاع السيرفر
print("🚀 [System] تم تفعيل نظام الترسانة السيادي (Supplier Panel) بنجاح.")
