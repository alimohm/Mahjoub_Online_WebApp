# coding: utf-8
from flask import Blueprint

# تعريف البلوبرينت (Blueprint) الخاص بلوحة القيادة
# هذا هو الذي يتم استيراده في المصنع المركزي (apps/__init__.py)
admin_dashboard_bp = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

# استيراد المسارات (Routes) هنا بعد تعريف البلوبرينت 
# لتجنب خطأ الاستيراد الدائري (Circular Import Error)
from . import routes
