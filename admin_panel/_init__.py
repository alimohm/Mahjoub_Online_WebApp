from flask import Blueprint

# 1. تعريف البلوبرنت الخاص ببرج الرقابة المركزية
# نحدد template_folder ليتعرف النظام على المجلد الذي يحتوي على login.html و dashboard.html
admin_panel = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# 2. استيراد المسارات (Routes) لربطها بالبلوبرنت
# نضع الاستيراد هنا في الأسفل لتجنب مشكلة الدوران البرمجي (Circular Import)
from . import routes
