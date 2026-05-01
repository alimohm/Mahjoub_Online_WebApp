from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # إذا كان المستخدم مسجلاً دخوله بالفعل، يتم توجيهه حسب رتبته
    if current_user.is_authenticated:
        return redirect_by_role(current_user)
    
    if request.method == 'POST':
        # جلب البيانات من نموذج تسجيل الدخول
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 1. البحث عن المستخدم أولاً في الترسانة الرقمية
        user = User.query.filter_by(username=username).first()
        
        # فحص وجود المستخدم
        if not user:
            flash(f'⚠️ تنبيه: اسم المستخدم "{username}" غير موجود في قاعدة البيانات.', 'danger')
            return redirect(url_for('admin.admin_login'))
        
        # 2. فحص كلمة المرور إذا وجدنا المستخدم
        if not user.check_password(password):
            flash('❌ كلمة المرور غير صحيحة. يرجى التأكد من مفتاح التشفير.', 'danger')
            return redirect(url_for('admin.admin_login'))
        
        # 3. التأكد من حالة الحساب (نشط أم معلق)
        if not user.is_active_account:
            flash('🚫 هذا الحساب معلق حالياً. يرجى مراجعة السيادة الإدارية.', 'warning')
            return redirect(url_for('admin.admin_login'))
        
        # إذا اجتاز كافة الفحوصات، يتم تسجيل الدخول بنجاح
        login_user(user)
        flash(f'أهلاً بك يا {user.username}. تم الولوج بنجاح إلى برج الرقابة.', 'success')
        return redirect_by_role(user)
            
    return render_template('login.html')

def redirect_by_role(user):
    """توجيه المستخدم بناءً على الصلاحيات السيادية (Admin/Supplier)"""
    if user.role == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    elif user.role == 'supplier':
        return redirect(url_for('supplier.dashboard'))
    
    return redirect(url_for('main.index'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """برج الرقابة المركزية - الإدارة العليا"""
    if current_user.role != 'admin':
        flash('عذراً، لا تملك صلاحيات الولوج إلى المناطق السيادية.', 'danger')
        return redirect(url_for('admin.admin_login'))
    
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة والولوج الآمن للخروج"""
    logout_user()
    flash('تم تسجيل الخروج بنجاح من النظام.', 'success')
    return redirect(url_for('admin.admin_login'))
