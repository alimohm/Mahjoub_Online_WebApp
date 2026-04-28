from flask import Blueprint

# تعريف البلوبرينت الخاص بالإدارة
# template_folder يخبر فلاسك أن يبحث عن الملفات السبعة داخل مجلد templates
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# استيراد الروابط بعد تعريف البلوبرينت لتجنب الاستيراد الدائري (Circular Import)
from . import routes
