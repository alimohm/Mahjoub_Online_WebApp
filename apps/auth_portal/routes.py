from flask import Blueprint, render_template, request, redirect, url_for, flash, session

# تعريف الـ Blueprint الخاص بنظام المصادقة
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # التحقق من بيانات الدخول السيادية
        # تم تعديل كلمة المرور لتصبح 123 بناءً على طلبك
        if username == 'ali_mahjoub' and password == '123':
            # وضع ختم الدخول في الجلسة
            session['is_authenticated'] = True  
            session['user_id'] = 'founder_ali'
            session['username'] = 'علي محجوب'
            
            # التوجه مباشرة إلى لوحة التحكم
            return redirect(url_for('admin.dashboard'))
        else:
            # رسالة تنبيه في حال الخطأ
            flash('تنبيه: بيانات الدخول غير صحيحة. يرجى المحاولة مرة أخرى.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    # مسح الجلسة تماماً عند الخروج لضمان الأمان السيادي للمنصة
    session.clear() 
    return redirect(url_for('auth.login'))
