from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User

# تعريف البلوبرينت وتحديد مكان القوالب بدقة
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        # منطق التحقق من الهوية هنا
        pass
    # البحث سيتم داخل admin_panel/templates/admin_panel/login.html
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_panel/dashboard.html')
