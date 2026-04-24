from flask import Blueprint

# 1. تعريف البلوبرنت (Blueprint) الخاص بمجتمع شركاء النجاح
# تأكد من إضافة template_folder لضمان وصول النظام لملفات الـ HTML الخاصة بالموردين
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (Routes) لربط العمليات بالبلوبرنت
# نضع الاستيراد في الأسفل لمنع مشكلة الاستيراد الدائري (Circular Import)
from . import routes
