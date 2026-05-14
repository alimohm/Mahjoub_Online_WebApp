# coding: utf-8
from flask import Blueprint
import os

# 1. تحديد مسار المجلد الحالي لضمان دقة الوصول للقوالب في Railway (Linux)
current_dir = os.path.dirname(os.path.abspath(__file__))
template_path = os.path.join(current_dir, 'templates')

# 2. إنشاء البلوبرينت الخاص ببوابة الدخول (Authentication Portal)
# تم تحديد template_folder بشكل صريح لتجنب أي تداخل بين الأقسام
auth_bp = Blueprint(
    'auth_bp', 
    __name__, 
    template_folder=template_path
)

# 3. كسر حلقة الاستيراد الدائري (Circular Import Fix)
# نستورد الملف المسؤول عن الروابط بعد تعريف البلوبرينت مباشرة
from . import routes
