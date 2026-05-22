# coding: utf-8
from flask import Blueprint

# تعريف البلوبرينت باسم 'wallet' ليتطابق مع ما تم تسجيله في apps/__init__.py
wallet_bp = Blueprint('wallet', __name__, template_folder='templates')

# استيراد ملف المسارات لضمان تسجيلها داخل البلوبرينت
from . import routes
