from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # إذا كان المستخدم مسجلاً بالفعل، يتم توجيهه حسب رتبته
    if current_user.is_authenticated:
        return redirect_to_dashboard(current_user)
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        # التحقق من صحة البيانات وجودة المستخدم
        if user and user.check_password(password):
            login_user(user)
            return redirect_to_dashboard(user)
        else:
            flash('عفواً.. مفتاح التشفير أو المعرف غير صحيح.', 'danger')
            
    return render_template('login.html')

def redirect_to_dashboard(user):
    """دالة مساعدة لتوجيه المستخدم بناءً على صلاحياته"""
    if user.is_admin:
        # توجيه لبرج الرقابة المركزية
        return redirect(url_for('admin.admin_dashboard'))
    elif hasattr(user, 'is_supplier') and user.is_supplier:
        # توجيه للوحة تحكم الموردين (VMS)
        return redirect(url_for('supplier.dashboard'))
    else:
        flash('ليس لديك صلاحيات وصول لهذا القطاع.', 'warning')
        return redirect(url_for('admin.admin_login'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # التأكد من أن الداخل هو المدير حصراً (علي محجوب)
    if not current_user.is_admin:
        flash('محاولة وصول غير مصرح بها لبرج الرقابة.', 'danger')
        return redirect(url_for('admin.admin_login'))
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم إنهاء الجلسة السيادية بنجاح.', 'success')
    return redirect(url_for('admin.admin_login'))
