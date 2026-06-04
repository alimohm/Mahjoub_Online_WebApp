# coding: utf-8
# 📂 apps/admin_dashboard/__init__.py

from flask import Blueprint

# تعريف الـ Blueprint الخاص بلوحة التحكم
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'  # المجلد الذي يحتوي على ملفات HTML الخاصة بالداشبورد
)

# استيراد المسارات لربطها بالـ Blueprint
from . import routes
