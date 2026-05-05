# admin_panel/__init__.py
from flask import Blueprint

# 1. تعريف الـ Blueprint الخاص بلوحة التحكم السيادية
# نقوم بتحديد مجلد القوالب والمجلد الثابت لضمان ظهور التصميم بشكل صحيح
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# 2. استيراد المسارات (Routes) والتوثيق (Auth)
# يجب أن يتم الاستيراد في نهاية الملف لتجنب خطأ الاستيراد الدائري (Circular Import)
try:
    from . import routes
    from . import auth
except ImportError as e:
    print(f"⚠️ تنبيه في لوحة التحكم: تعذر استيراد المسارات. الخطأ: {e}")
