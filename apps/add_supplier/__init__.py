from flask import Blueprint

# تعريف الـ Blueprint
add_supplier_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates',
    url_prefix='/admin/suppliers'
)

# الربط بالمسارات
from . import routes
