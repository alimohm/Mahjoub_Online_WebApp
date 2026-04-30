from flask import Blueprint

# 1. تعريف البلوبرنت
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')

# 2. استدعاء المسارات لربطها بالبلوبرنت (هذا السطر هو المحرك)
from . import routes
