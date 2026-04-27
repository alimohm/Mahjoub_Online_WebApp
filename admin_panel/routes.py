from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from . import admin_bp
from core import db
from core.models import User # استيراد موديل المستخدمين للتحقق من الصلاحيات

# --- بوابة دخول الإدارة (برج الرقابة) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # إذا كان المدير مسجلاً دخوله بالفعل، يذهب للوحة التحكم مباشرة
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم بشرط أن يكون دوره "admin"
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            print(f"✅ نفاذ معتمد للمدير: {username}")
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('⚠️ فشل التحقق السيادي: بيانات الإدارة غير صحيحة.', 'danger')
            
    # استدعاء القالب الكحلي الذي صممناه
    return render_template('admin_panel/login.html')

# --- لوحة التحكم المركزية (الداشبورد) ---
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # حماية إضافية: التأكد أن الداخل هو "admin" فعلاً وليس مورد حاول تخمين الرابط
    if current_user.role != 'admin':
        flash('🚫 غير مسموح لك بدخول منطقة الرقابة المركزية.', 'danger')
        return redirect(url_for('supplier_panel.login'))
        
    return render_template('admin_panel/dashboard.html')

# --- تسجيل خروج الإدارة ---
@admin_bp.route('/logout')
def admin_logout():
    logout_user()
    flash('🔒 تم إغلاق برج الرقابة وتأمين النظام.')
    return redirect(url_for('admin_panel.admin_login'))
