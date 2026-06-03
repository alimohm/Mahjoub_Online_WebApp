# coding: utf-8
# 📂 apps/statement/__init__.py

from flask import Blueprint

# تعريف الـ Blueprint
statement_blueprint = Blueprint(
    'statement_blueprint', 
    __name__, 
    template_folder='templates', 
    static_folder='static'
)

# استيراد الـ routes لتسجيل المسارات
from . import routes
