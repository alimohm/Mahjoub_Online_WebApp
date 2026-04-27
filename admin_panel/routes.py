from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from . import admin_bp  # استيراد كائن البلوبرينت من ملف __init__.py المحيط
from core import db
from core.models import User

# --- بوابة دخول الإدارة (برج الرقابة المركزية) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # 1. إذا كان القائد مسجلاً دخوله بالفعل ولديه صلاحية admin
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_panel.admin_dashboard'))
        # إذا كان المستخدم مسجلاً بدور آخر (مثل مورد)، نقوم بتسجيل خروجه ليدخل بحساب الإدارة
        logout_user()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # البحث عن المستخدم في قاعدة البيانات بشرط أن يكون دوره "admin"
        user = User.query.filter_by(username=username, role='admin').first()

        # التحقق من وجود المستخدم وصحة شفرة العبور
        if user and user.check_password(password):
            login_user(user)
            print(f"✅ نفاذ معتمد لبرج الرقابة: {username}")
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('⚠️ شفرة العبور أو معرف القائد غير مطابق للسجلات السيادية.', 'error')

    # عرض القالب الكحلي الخاص بالإدارة
    return render_template('admin_panel/login.html')

# --- لوحة التحكم المركزية (الداشبورد) ---
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # حماية سيادية إضافية: التأكد أن المستخدم "admin" فعلاً
    if current_user.role != 'admin':
        flash('🚫 غير مسموح لك بدخول منطقة الرقابة المركزية.', 'danger')
        return redirect(url_for('admin_panel.admin_login'))

    return render_template('admin_panel/dashboard.html')

# --- تسجيل خروج الإدارة ---
@admin_bp.route('/logout')
@login_required
def admin_logout():
    logout_user()
    flash('🔒 تم إغلاق برج الرقابة وتأمين النظام بنجاح.')
    return redirect(url_for('admin_panel.admin_login'))
