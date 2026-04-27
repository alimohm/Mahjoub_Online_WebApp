from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from core.models import User
# استيراد البلوبرنت من نفس المجلد
from . import admin_bp 

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and check_password_hash(user.password, password):
            session['user_type'] = 'admin'
            login_user(user)
            return redirect(url_for('admin_panel.dashboard'))
        flash('بيانات الدخول غير صحيحة', 'danger')
        
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin_panel/dashboard.html')
