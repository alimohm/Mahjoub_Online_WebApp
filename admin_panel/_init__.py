from flask import Blueprint

# تعريف البلوبرنت فقط هنا
admin_panel = Blueprint('admin_panel', __name__, template_folder='templates')
