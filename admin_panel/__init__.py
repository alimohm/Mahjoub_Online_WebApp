from flask import Blueprint

# تعريف الـ Blueprint ليكون مستقلاً بمجلده وقوالبه
admin_bp = Blueprint('admin', __name__, template_folder='templates')

# استيراد الروابط والمنطق بعد التعريف لربطها بالـ Blueprint
from . import routes
