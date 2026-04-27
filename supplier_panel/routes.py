from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from . import supplier_bp
from core import db
from core.models import User, Product

# --- بوابة الدخول ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        # إذا كان مسجلاً، يتم توجيهه حسب حالته
        if current_user.status == 'approved':
            return redirect(url_for('supplier_panel.dashboard'))
        return redirect(url_for('supplier_panel.waiting_approval'))
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username, role='supplier').first()
        
        if user and user.check_password(password):
            login_user(user)
            # فحص الحالة بعد الدخول مباشرة
            if user.status == 'approved':
                return redirect(url_for('supplier_panel.dashboard'))
            else:
                return redirect(url_for('supplier_panel.waiting_approval'))
        else:
            flash('⚠️ شفرة العبور غير مطابقة للسجلات السيادية.', 'error')
            
    return render_template('supplier_panel/supplier_login.html')

# --- غرفة الانتظار والتدقيق ---
@supplier_bp.route('/waiting-approval')
@login_required
def waiting_approval():
    # إذا تم اعتماد المورد وهو في هذه الصفحة، يتم توجيهه تلقائياً للداشبورد
    if current_user.status == 'approved':
        return redirect(url_for('supplier_panel.dashboard'))
    return render_template('supplier_panel/waiting_approval.html')

# --- لوحة التحكم (مع حماية إضافية) ---
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    # حماية: منع المورد غير المعتمد من دخول الداشبورد حتى لو عرف الرابط
    if current_user.status != 'approved':
        return redirect(url_for('supplier_panel.waiting_approval'))
        
    products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('supplier_panel/dashboard.html', products=products)

# --- تسجيل الخروج ---
@supplier_bp.route('/logout')
def logout():
    logout_user()
    flash('🔒 تم تأمين الجلسة والخروج بنجاح.')
    return redirect(url_for('supplier_panel.login'))
