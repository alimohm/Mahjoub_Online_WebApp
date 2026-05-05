# admin_panel/__init__.py
from flask import Blueprint

# 1. تعريف الـ Blueprint أولاً كقاعدة أساسية
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات والتوثيق في النهاية لكسر حلقة التداخل (Circular Import)
# هذا يضمن أن نظام "محجوب أونلاين" سيعمل بدون انهيار عند التشغيل
from . import routes
from . import auth
