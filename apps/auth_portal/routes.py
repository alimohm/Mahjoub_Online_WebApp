# coding: utf-8
# 🔑 بوابة النفاذ السيادية - منصة محجوب أونلاين 2026

from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash
from datetime import datetime
from apps.extensions import db
from apps.models.admin_db import AdminUser

# استيراد البلوبرينت من نفس المجلد
from . import auth_blueprint

@auth_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    # منع الدخول المتكرر إذا كان المالك مسجلاً بالفعل
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = AdminUser.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password_hash, password):
            # التأكد من امتلاك صلاحيات (Owner) أو (Admin)
            if user.role in ['Owner', 'Admin']:
                login_user(user)
                
                # تحديث سجل الدخول
                user.last_login = datetime.utcnow()
                db.session.commit()
                
                flash('مرحباً بك في سوقك الذكي.', 'success')
                return redirect(url_for('admin_dashboard.dashboard'))
            else:
                flash('ليس لديك صلاحيات الوصول لهذه المنطقة السيادية.', 'warning')
        else:
            flash('بيانات الدخول غير صحيحة، يرجى التحقق من الهوية الرقمية.', 'danger')
    
    return render_template('auth/login.html')

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج من المنطقة السيادية بنجاح.', 'info')
    return redirect(url_for('auth_portal.login'))
