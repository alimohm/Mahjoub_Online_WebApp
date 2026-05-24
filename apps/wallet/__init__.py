# coding: utf-8
from flask import Blueprint

# تعريف البلوبرينت مع تحديد مجلد القوالب الخاص به
# هذا يحل مشكلة TemplateNotFound لأن Flask سيبحث داخل مجلد templates في هذا المسار
wallet_blueprint = Blueprint(
    'wallet', 
    __name__, 
    template_folder='templates'
)

# لا تقم باستيراد routes هنا لتجنب Circular Import (حلقة الاستيراد)
# سيتم استيراده في ملف apps/__init__.py الرئيسي عند التسجيل
