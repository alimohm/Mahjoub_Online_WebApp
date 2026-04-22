from flask import Blueprint, render_template

# تعريف بوابة الموردين
supplier_bp = Blueprint('supplier', __name__, 
                        template_folder='templates',
                        static_folder='static')

@supplier_bp.route('/supplier/login')
def login():
    return "<h1>صفحة دخول الموردين - قريباً</h1>"
