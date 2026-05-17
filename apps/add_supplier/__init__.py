# coding: utf-8
# 📦 محرك إدارة وتعميد الموردين - محجوب أونلاين 2026

from flask import Blueprint
import os

# 1. تحديد المسار المطلق للمجلد لضمان استقرار بيئة Linux
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت بالاسم المعتمد 'admin_suppliers' لمنع أخطاء الـ BuildError
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder=template_path
)

# 3. استدعاء المسارات بشكل متأخر وآمن لحماية العزل التام ومنع Circular Import
try:
    from . import routes
    print("✅ تم ربط محرك الموردين بنجاح وعمّدت المسارات.")
except ImportError as e:
    print(f"⚠️ تنبيه: تعذر تحميل مسارات الموردين داخلياً: {e}")
