from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User 
from core import db # استيراد قاعدة البيانات إذا احتجت لتسجيل عمليات الدخول

# تأكد أن اسم البلوبرنت هنا هو 'admin_bp' ليتطابق مع ما سجلناه في core/__init__.py
admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    # 1. إذا كان القائد مسجلاً بالفعل، انقله فوراً للوحة التحكم
    if current_user.is_authenticated and current_user.is_admin:
        return redirect(url_for('admin.admin_dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 2. البحث عن المستخدم في الترسانة المركزية
        user = User.query.filter_by(username=username).first()
        
        # 3. منطق التحقق الصارم
        if not user:
            flash('عفواً.. "معرف القائد" الذي أدخلته غير مسجل في النظام.', 'danger')
        elif not user.is_admin:
            flash('ليس لديك صلاحية الوصول إلى برج الرقابة المركزية.', 'warning')
        else:
            # التحقق من كلمة المرور (تأكد أن الموديل يحتوي على check_password)
            if user.check_password(password):
                login_user(user)
                return redirect(url_for('admin.admin_dashboard'))
            else:
                flash('خطأ في "مفتاح التشفير".. يرجى التأكد من كلمة المرور.', 'danger')
            
    return render_template('login.html')

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not current_user.is_admin:
        return redirect(url_for('admin.admin_login'))
    return render_template('dashboard.html')

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم إنهاء الجلسة السيادية بنجاح.', 'success')
    return redirect(url_for('admin.admin_login'))
