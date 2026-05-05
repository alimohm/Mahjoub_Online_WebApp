from flask import Blueprint

# تعريف الـ Blueprint
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# استيراد المسارات في الأسفل لكسر "الدائرة" المسببة للخطأ
from . import routes
