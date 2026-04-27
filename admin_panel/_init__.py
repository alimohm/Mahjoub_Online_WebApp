from flask import Blueprint

# تعريف البلوبرنت وتحديد أماكن القوالب والملفات الثابتة
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد الروابط في الأسفل لتجنب تداخل الاستدعاء مع core
from . import routes

# تصدير الكائن ليكون متاحاً للنواة
__all__ = ['admin_bp']
