# coding: utf-8
from flask import Blueprint

# 👑 تعريف البلوبرينت
admin_wallet = Blueprint(
    'admin_wallet', 
    __name__, 
    template_folder='templates'
)

# 🛡️ استيراد المسارات هنا (هذا صحيح طالما أنك لا تستورد 'db' أو 'models' داخل routes.py في مستوى الملف العلوي)
from . import routes
