from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from core.models.user import User
from core import db

# تعريف البلوبرينت للموردين - هذا السطر ينهي مشكلة المسارات نهائياً
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

# --- مسارات الدخول (Supplier Auth) ---

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    # إذا كان المورد مسجلاً دخوله بالفعل، يتم توجيهه للوحة تحكمه
    if current_user.is_authenticated and current_user.role == 'supplier':
        return redirect(url_for('supplier_panel.supplier_dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث عن المورد والتأكد من دوره في النظام
        user = User.query.filter_by(username=username, role='supplier').first()
        
        if user and user.check_password(password):
            # التأكد من أن الحساب "معمد" (Approved) من قبل الإدارة
            if user.status == 'approved':
                login_user(user)
                flash('مرحباً بك في منصة التوريد الخاصة بك.', 'success')
                return redirect(url_for('supplier_panel.supplier_dashboard'))
            else:
                flash('حسابك لا يزال قيد المراجعة من قبل الإدارة.', 'warning')
        else:
            flash('بيانات الدخول غير صحيحة.', 'danger')

    # سيبحث Flask في supplier_panel/templates/supplier_panel/login.html
    return render_template('supplier_panel/login.html')

@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    logout_user()
    flash('تم تسجيل الخروج من بوابة الموردين.', 'info')
    return redirect(url_for('supplier_panel.supplier_login'))

# --- مسارات العمليات (Supplier Dashboard) ---

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    # حماية المسار: التأكد أن المستخدم "مورد" وليس "مدير"
    if current_user.role != 'supplier':
        return redirect(url_for('admin_panel.admin_login'))
        
    return render_template('supplier_panel/dashboard.html')

@supplier_bp.route('/my-products')
@login_required
def my_products():
    if current_user.role != 'supplier':
        return redirect(url_for('supplier_panel.supplier_login'))
    return render_template('supplier_panel/my_products.html')

@supplier_bp.route('/add-product')
@login_required
def add_product():
    if current_user.role != 'supplier':
        return redirect(url_for('supplier_panel.supplier_login'))
    return render_template('supplier_panel/add_product.html')
