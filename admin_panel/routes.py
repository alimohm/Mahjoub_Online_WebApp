from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # هنا تضع منطق التحقق الخاص بك (مثال مؤقت)
        if username == "ali_admin" and password == "9046":
            # تفاصيل تسجيل الدخول...
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('خطأ في بيانات العبور السيادية', 'danger')
            
    # لاحظ المسار هنا: يتوافق تماماً مع هيكل مجلداتك
    return render_template('admin_panel/login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return "مرحباً بك في برج الرقابة المركزية"
