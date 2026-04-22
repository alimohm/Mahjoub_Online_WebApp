import os
from flask import Blueprint, render_template

# تحديد المسار الفعلي لمجلد القوالب لضمان وصول Flask إليه
current_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(current_dir, 'templates')

admin_bp = Blueprint('admin', __name__, 
                     template_folder=template_dir)

@admin_bp.route('/admin/login')
def login():
    # يبحث الآن داخل admin_panel/templates/admin/login.html
    return render_template('admin/login.html')

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('admin/wallets.html')
