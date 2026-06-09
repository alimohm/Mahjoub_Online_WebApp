# 📂 apps/wallet/__init__.py
from flask import Blueprint

# تعريف الـ Blueprint للمحفظة
# 'wallet_app' هو الاسم الذي سنستخدمه في تسجيل الـ Blueprint في __init__.py الرئيسي
# template_folder='templates' يحدد أن القوالب الخاصة بهذا الجزء موجودة في مجلد templates الفرعي
wallet_app = Blueprint('wallet_app', __name__, template_folder='templates')

# استيراد ملف المسارات (Routes) في نهاية الملف 
# هذا ضروري جداً لكي يتعرف Flask على المسارات الموجودة في routes.py
from apps.wallet import routes
