# apps/add_supplier/__init__.py
# coding: utf-8

from flask import Blueprint

# إنشاء كائن البلوبرينت الخاص بإضافة الموردين لـ "منصة محجوب أونلاين"
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates'
)

# استدعاء ملف الـ routes في الأسفل لحقن المسارات داخل البلوبرينت بعد إنشائه
from . import routes
