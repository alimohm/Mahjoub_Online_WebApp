from flask import Blueprint

# تعريف الـ Blueprint للقيادة المركزية (محجوب أونلاين)
# تم دمج الإعدادات لضمان تحميل موارد الهوية البصرية (الأرجواني والذهبي) بشكل صحيح
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    static_url_path='/admin/static'
)

# استيراد الروابط (Routes) في الأسفل حصراً
# هذا الإجراء ضروري جداً لتجنب مشاكل "الاستيراد الدائري" (Circular Imports) 
# التي تسببت في انهيار السيرفر سابقاً
from . import routes
