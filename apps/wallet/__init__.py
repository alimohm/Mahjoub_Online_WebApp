# coding: utf-8
from flask import Blueprint

# هذا التعريف هو الأساس لربط الروابط. 
# يجب أن يكون الاسم 'wallet' مطابقاً لما هو مسجل في apps/__init__.py
from flask import Blueprint
wallet_bp = Blueprint('wallet', __name__, template_folder='templates')
from . import routes

# هذا السطر ضروري جداً لكي يتعرف التطبيق على الدوال المعرفة في ملف routes.py
from . import routes
