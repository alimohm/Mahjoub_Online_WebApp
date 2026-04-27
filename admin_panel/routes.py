from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from . import admin_bp
from core.models import User, db

# --- بوابة دخول الإدارة المستقلة ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('⚠️ فشل التحقق من الهوية القيادية.', 'error')
            
    return render_template('admin_panel/login.html') # صفحة دخول خاصة بالمدير

# --- لوحة التحكم ---
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    
    pending_suppliers = User.query.filter_by(role='supplier', status='pending').all()
    return render_template('admin_panel/dashboard.html', suppliers=pending_suppliers)

@admin_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))
