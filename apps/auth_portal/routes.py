from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.admin_db import AdminUser  # استيراد نموذج المستخدمين من مجلد models

auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username_input = request.form.get('username')
        password_input = request.form.get('password')

        # البحث عن المستخدم في سجلات المنظومة
        user = AdminUser.query.filter_by(username=username_input).first()

        if user:
            # مطابقة كلمة السر يدوياً كما هي في قاعدة البيانات حالياً
            if user.password == password_input:
                session['user_id'] = user.id
                session['username'] = user.username
                flash(f'مرحباً بك يا {user.username}، تم الدخول بنجاح', 'success')
                return redirect(url_for('admin.index')) # التوجه للوحة التحكم
            else:
                flash('فشل الدخول: كلمة المرور غير صحيحة.', 'danger')
        else:
            flash('تنبيه: اسم المستخدم هذا غير موجود في النظام.', 'warning')
            
        return redirect(url_for('auth.login'))

    return render_template('auth/login.html')
