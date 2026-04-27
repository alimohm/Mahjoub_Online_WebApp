from flask import Blueprint

# تعريف البلوبرنت بدون استيراد أي شيء آخر في الأعلى
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# الاستيراد يكون في الأسفل تماماً
from . import routes
