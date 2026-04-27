from flask import Blueprint

# تعريف البلوبرنت
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

# استيراد المسارات لربطها بالبلوبرنت
from . import routes
