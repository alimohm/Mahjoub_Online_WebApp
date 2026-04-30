from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_blueprint

# استيراد الموديلات من المسارات الجديدة حسب هيكلتك
from core.models.user import User
from core.models.supplier import Supplier
from core.models.product import Product
from core import db

# --- بوابة الولوج ---
@admin_blueprint.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and getattr(current_user, 'role', None) == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            flash('أهلاً بك يا علي. تم تفعيل الصلاحيات السيادية.', 'success')
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('خطأ في البيانات.. يرجى التحقق.', 'danger')

    return render_template('admin_panel/login.html')

# --- لوحة التحكم ---
@admin_blueprint.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_panel/dashboard.html')

# --- تسجيل الخروج ---
@admin_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))
