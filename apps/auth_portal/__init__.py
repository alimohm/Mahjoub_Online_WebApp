# coding: utf-8
# 🔑 بوابة النفاذ السيادية - منصة محجوب أونلاين 2026

from flask import Blueprint
import os

# 1. تحديد مسار المجلد الحالي لضمان دقة الوصول للقوالب في البيئات السحابية (Linux)
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت الموحد والمطابق تماماً لما يتم استدعاؤه في المصنع المركزي
# الاسم 'auth_portal' هنا يجب أن يطابق الاسم المستخدم في app.register_blueprint في __init__.py
auth_blueprint = Blueprint(
    'auth_portal', 
    __name__, 
    template_folder='templates' # تم التبسيط لضمان التوافق مع هيكلية Flask القياسية
)

# 3. كسر حلقة الاستيراد الدائري واستدعاء المسارات بشكل آمن
from . import routes
