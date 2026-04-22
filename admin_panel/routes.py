import os
from flask import Blueprint, render_template

# الحصول على المسار الكامل لمجلد templates الموجود بجانب هذا الملف (routes.py)
# المسار المتوقع: admin_panel/templates
base_dir = os.path.abspath(os.path.dirname(__file__))
template_dir = os.path.join(base_dir, 'templates')

# تعريف البلوبرنت مع تحديد مسار القوالب بشكل مطلق
admin_bp = Blueprint('admin', __name__, template_folder=template_dir)

@admin_bp.route('/admin/login')
def login():
    # Flask سيبحث الآن مباشرة داخل admin_panel/templates/
    # وبما أن login.html هناك، سيعمل فوراً.
    return render_template('login.html')

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('wallets.html')
