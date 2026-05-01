from flask import Blueprint

# تعريف البلوبرنت الخاص بالإدارة والتحكم
admin_bp = Blueprint(
    'admin', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

# استيراد المسارات (المنطق) لربطها بالبلوبرنت
from . import routes
