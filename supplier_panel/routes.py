from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app as app
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models.user import User

# 1. تعريف البلوبرينت الخاص بالموردين
# تأكد أن اسم المجلد الفرعي للقوالب هو supplier_panel
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

# 2. مسار تسجيل الدخول (Login)
@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    # منع المستخدم المسجل (كمورد) من العودة لصفحة الدخول
    if current_user.is_authenticated:
        if current_user.role == 'supplier':
            return redirect(url_for('supplier_panel.supplier_dashboard'))
        elif current_user.role == 'admin':
            return redirect(url_for('admin_panel.admin_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المستخدم في قاعدة البيانات برتبة مورد فقط
        user = User.query.filter_by(username=username, role='supplier').first()
        
        if user and user.check_password(password):
            if user.status == 'approved':
                login_user(user)
                flash(f'مرحباً بك في بوابة التوريد، {user.username}', 'success')
                return redirect(url_for('supplier_panel.supplier_dashboard'))
            else:
                flash('حسابك لا يزال قيد المراجعة من قبل الإدارة المركزية.', 'warning')
        else:
            flash('بيانات الدخول غير صحيحة أو الحساب غير مسجل كمورد.', 'danger')

    # استدعاء القالب من المجلد الفرعي: templates/supplier_panel/login.html
    return render_template('supplier_panel/login.html')

# 3. لوحة تحكم المورد (Dashboard)
@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    # حماية سيادية: التأكد من أن المستخدم ليس مديراً يحاول التطفل
    if current_user.role != 'supplier':
        flash('هذا القسم مخصص للموردين فقط.', 'danger')
        return redirect(url_for('admin_panel.admin_dashboard'))
        
    # استدعاء القالب من المجلد الفرعي: templates/supplier_panel/dashboard.html
    return render_template('supplier_panel/dashboard.html', user=current_user)

# 4. تسجيل الخروج (Logout)
@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    logout_user()
    flash('تم تسجيل الخروج من بوابة الموردين بنجاح.', 'info')
    return redirect(url_for('supplier_panel.supplier_login'))
