from flask import Blueprint, render_template, request, redirect, url_for, flash

# تعريف البلوبرنت الخاص بالتوثيق
auth_bp = Blueprint('auth', __name__, template_folder='templates')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # توثيق القائد (سيتم ربطه بـ Engine الموديلات لاحقاً)
        if username == 'ali_mahjoub' and password == 'الملك_2026':
            return redirect(url_for('admin.dashboard'))
        else:
            flash('تنبيه أمني: بيانات الدخول غير صحيحة.', 'danger')
            
    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    # إنهاء الجلسة والعودة للبوابة
    return redirect(url_for('auth.login'))
  
