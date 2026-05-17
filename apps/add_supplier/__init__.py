# coding: utf-8
# 📦 محرك إدارة وتعميد الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint
import os

# 1. تحديد المسار المطلق للمجلد لضمان استقرار قراءة القوالب على السيرفر السحابي
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء وتعميد البلوبرينت بالاسم المعتمد في النواة ولوحة التحكم لمنع أخطاء الـ BuildError
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder=template_path
)

# 3. استدعاء ملف المسارات (routes) بشكل متأخر وآمن لحماية العزل التام ومنع الـ Circular Import
try:
    from . import routes
    print("✅ تم ربط محرك الموردين [admin_suppliers] بنجاح وعُمّدت كافة المسارات السيادية.")
except ImportError as e:
    print(f"⚠️ تنبيه حوكمي: تعذر تحميل مسارات الموردين داخلياً، تفاصيل الخطأ: {e}")
