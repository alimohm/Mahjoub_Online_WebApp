from flask import render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from admin_panel import admin_panel
from core.models import User, Supplier, Product, db
from core.utils.security import admin_required

# --- بوابة تسجيل الدخول (نظام الولوج السيادي) ---
@admin_panel.route('/login', methods=['GET', 'POST'])
def admin_login():
    # منع الدخول المتكرر إذا كان القائد مسجلاً بالفعل
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.dashboard'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث في قاعدة بيانات Render
        user = User.query.filter_by(username=username, role='admin').first()

        # التحقق من مفتاح التشفير (كلمة المرور)
        if user and user.check_password(password):
            login_user(user)
            flash('تم تفعيل الولوج السيادي بنجاح.', 'success')
            return redirect(url_for('admin_panel.dashboard'))
        else:
            flash('فشل في التحقق من الهوية.. تأكد من معرف القائد أو مفتاح التشفير.', 'danger')

    return render_template('admin_panel/login.html')

# --- برج الرقابة المركزية (لوحة التحكم) ---
@admin_panel.route('/dashboard')
@login_required
@admin_required
def dashboard():
    # إحصائيات حية متوافقة مع تصميم Dashboard الخاص بك
    stats_data = {
        'orders_count': 0, # سيتم ربطه بجدول الطلبات لاحقاً
        's_count': Supplier.query.count(),
        'total_balance': 0.00, # محرك العملات والسيولة
        'p_count': Product.query.count()
    }
    
    # جلب آخر العمليات السيادية (فارغة حالياً حتى بناء جدول العمليات)
    recent_transactions = []
    
    return render_template('admin_panel/dashboard.html', 
                           orders_count=stats_data['orders_count'],
                           s_count=stats_data['s_count'],
                           total_balance=stats_data['total_balance'],
                           p_count=stats_data['p_count'],
                           transactions=recent_transactions)

# --- إدارة شركاء الترسانة (الموردين) ---
@admin_panel.route('/manage-suppliers')
@login_required
@admin_required
def manage_suppliers():
    # جلب جميع الموردين المسجلين في النظام اليمني
    all_suppliers = Supplier.query.all()
    return render_template('admin_panel/manage_suppliers.html', suppliers=all_suppliers)

# --- نظام الاعتماد الفوري للمتاجر ---
@admin_panel.route('/verify-supplier/<int:supplier_id>')
@login_required
@admin_required
def verify_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    supplier.is_verified = True
    db.session.commit()
    flash(f'تم منح الاعتماد لمتجر: {supplier.store_name}.', 'success')
    return redirect(url_for('admin_panel.manage_suppliers'))

# --- إنهاء الجلسة الآمنة ---
@admin_panel.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم إغلاق البوابة السيادية بنجاح.', 'info')
    return redirect(url_for('admin_panel.admin_login'))
