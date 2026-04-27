from flask import Blueprint

# 1. تعريف البلوبرنت (هذا هو السطر الذي يبحث عنه السيرفر وفشل في إيجاده)
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (routes) لربطها بالبلوبرنت
# ملاحظة: يجب أن يكون الاستيراد بعد تعريف admin_bp لتجنب الأخطاء
from . import routes
