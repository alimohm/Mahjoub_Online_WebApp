from flask import Blueprint

# هذا السطر هو الذي "يعمد" المجلد كبوابة إدارة
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

from . import routes
