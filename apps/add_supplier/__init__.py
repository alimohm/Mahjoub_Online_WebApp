# coding: utf-8
# ⚙️ ملف تهيئة وحدة إدارة الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint

# تعريف الـ Blueprint
# الاسم الأول 'add_supplier' يجب أن يتطابق مع ما تستخدمه في url_for
admin_suppliers_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المسارات (Routes) بعد تعريف الـ Blueprint لتجنب التداخل الدائري (Circular Import)
from . import routes
