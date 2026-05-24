# coding: utf-8
from flask import Blueprint

# تعريف الـ Blueprint بالاسم المعتمد 'add_supplier' الحاكم لعمليات الـ url_for
admin_suppliers_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates',
    static_folder='static'  # تأمين مسار الملفات الساكنة الخاصة بالموديل عند الحاجة
)

# استدعاء المسارات (Routes) بشكل سفلي لربطها بالـ Blueprint بعد تعريفه لتجنب الـ Circular Import
from . import routes
