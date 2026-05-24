# coding: utf-8
from flask import Blueprint

# تعريف الـ Blueprint بالاسم المعتمد في الـ url_for لمنع تكرار أخطاء البناء
admin_suppliers_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates'
)

# استدعاء المسارات (Routes) لربطها بالـ Blueprint بعد تعريفه لتجنب الـ Circular Import
from . import routes
