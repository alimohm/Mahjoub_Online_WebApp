# coding: utf-8
from flask import Blueprint

# تعريف البلوبرينت هنا مع تحديد مجلد القوالب
wallet_blueprint = Blueprint(
    'wallet', 
    __name__, 
    template_folder='templates'
)

# لا تستورد routes هنا، سيتم الاستيراد في ملف المصنع الرئيسي
