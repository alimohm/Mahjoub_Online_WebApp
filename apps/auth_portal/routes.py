# coding: utf-8
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from apps.extensions import db
# 1. إزالة الاستيراد العلوي للموديل 
# from apps.models.admin_db import AdminUser 

# استيراد البلوبرينت
from . import auth_blueprint

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # 2. استيراد الموديل داخل الدالة فقط (Lazy Import)
    from apps.models.admin_db import AdminUser
    
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        username = str(request.form.get('username', '')).strip()
        password = request.form.get('password', '')
        
        user = AdminUser.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if user.role in ['Owner', 'Admin']:
                login_user(user)
                user.last_login = db.func.current_timestamp()
                db.session.commit()
                return redirect(url_for('admin_dashboard.dashboard'))
            else:
                flash('ليس لديك صلاحيات الوصول.', 'warning')
        else:
            flash('بيانات الدخول غير صحيحة.', 'danger')
    
    return render_template('auth/login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth_portal.login'))
