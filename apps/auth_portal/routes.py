from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# تعريف الـ Blueprint مع تحديد مجلد القوالب الخاص بـ auth_portal
auth_bp = Blueprint(
    'auth_portal', 
    __name__, 
    template_folder='templates'
)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # منطق التحقق من الهوية (مثال أولي)
        # يمكنك لاحقاً ربطها بقاعدة البيانات الخاصة بالمنصة
        if username == 'admin' and password == 'mahjoub@2026':
            session['user_id'] = 'admin_1'
            session['username'] = username
            
            # التوجه إلى لوحة التحكم الإدارية بعد النجاح
            return redirect(url_for('admin_dashboard.index'))
        else:
            flash('فشل التحقق: اسم المستخدم أو كلمة المرور غير صحيحة', 'danger')
            return redirect(url_for('auth_portal.login'))

    # عرض صفحة الدخول من المسار auth/login.html
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('تم تسجيل الخروج من النظام السيادي بنجاح', 'success')
    return redirect(url_for('auth_portal.login'))
