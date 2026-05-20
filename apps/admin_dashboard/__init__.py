# coding: utf-8
# 🛡️ محرك لوحة التحكم - منصة محجوب أونلاين 2026

from flask import Blueprint

# تعريف الـ Blueprint:
# 'admin_dashboard': الاسم الذي سنستخدمه في url_for
# __name__: يحدد مسار الملف الحالي
# template_folder='templates': يخبر Flask أن يبحث عن قوالب HTML داخل هذا المجلد
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# استيراد المسارات (Routes) بعد تعريف الـ Blueprint
# هذا الترتيب ضروري جداً لتجنب خطأ Circular Import (الدوران في الاستيراد)
from . import routes
