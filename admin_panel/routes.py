import os
from flask import Blueprint, render_template

# الحصول على المسار الكامل للمجلد الذي يحتوي على هذا الملف (admin_panel)
base_path = os.path.dirname(os.path.abspath(__file__))

# تحديد أن مجلد القوالب هو المجلد الموجود داخل admin_panel واسمه templates
# المسار الفعلي سيكون: /app/admin_panel/templates
template_full_path = os.path.join(base_path, 'templates')

admin_bp = Blueprint('admin', __name__, template_folder=template_full_path)

@admin_bp.route('/admin/login')
def login():
    # بما أننا حددنا المجلد أعلاه، Flask سيبحث بداخله مباشرة عن login.html
    return render_template('login.html')

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('dashboard.html')

@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('wallets.html')
