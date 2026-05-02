from flask import Blueprint

# تعريف الـ Blueprint للقيادة المركزية (محجوب أونلاين)
# تم إضافة static_folder لضمان تحميل موارد الهوية البصرية (الأرجواني والذهبي)
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)

# استيراد الروابط (Routes) بعد التعريف لتجنب مشاكل الاستيراد الدائري (Circular Imports)
# وضمان ربط كافة مسارات "مركز المراقبة" بالـ Blueprint
from . import routes

from flask import Blueprint

# 1. تعريف الـ Blueprint الخاص بلوحة الإدارة
# نحدد اسم الـ Blueprint ومسار القوالب (templates) الخاص به
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد الملفات الفرعية لربطها بالـ Blueprint
# ملاحظة: يجب وضع هذا الاستيراد في الأسفل لتجنب مشكلة "الاستيراد الدائري" (Circular Import)
from . import routes
