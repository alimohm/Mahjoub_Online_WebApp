# admin_panel/__init__.py
from flask import Blueprint

# 1. إعلان الهوية السيادية لمنطقة الإدارة (Blueprint Definition)
# تم تحديد مجلدات القوالب والملفات الثابتة لضمان عزل بيئة الإدارة عن الواجهة العامة
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static',
    url_prefix='/admin'  # إضافة البادئة لضمان أن كل روابط الإدارة تبدأ بـ /admin
)

# 2. بروتوكول كسر التداخل (Circular Import Protection)
# استيراد المكونات بعد تعريف Blueprint يضمن أن Flask يرى 'admin_bp' أولاً
from . import routes           # المسارات الرئيسية والـ Dashboard
from . import auth             # نظام تسجيل الدخول والتحقق السيادي
from . import manage_suppliers  # منطق إدارة وترسانة الموردين

# ملاحظة سيادية: 
# تأكد من تسجيل هذا الـ Blueprint في ملف التطبيق الرئيسي app.py 
# عبر الكود: app.register_blueprint(admin_bp)
