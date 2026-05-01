from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
# استيراد موديل المستخدم من الترسانة المركزية
from core.models.user import User 

# 1. تعريف البلوبرنت مع تحديد مجلد القوالب بدقة
# بما أنك وضعت login.html داخل templates مباشرة، Flask سيبحث عنها هناك
admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """
    صفحة تسجيل دخول الإدارة.
    المسار الحالي للقالب: admin_panel/templates/login.html
    """
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, is_admin=True).first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin.admin_dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة أو ليس لديك صلاحية مدير.', 'danger')
            
    # تم تصحيح المسار هنا ليكون login.html مباشرة
    return render_template('login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """
    لوحة التحكم لإدارة الموردين والعمليات.
    المسار المتوقع للقالب: admin_panel/templates/dashboard.html
    """
    if not current_user.is_admin:
        return redirect(url_for('admin.admin_login'))
    
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin.admin_login'))
