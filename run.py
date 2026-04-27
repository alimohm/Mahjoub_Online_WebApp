from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user, logout_user, login_user
from . import admin_bp
from core import db
# استيراد المستخدم من المسار الجديد للموديلات
from core.models.user import User
# استيراد الموديلات الأخرى حسب الحاجة (مثل المنتجات)
from core.models.product import Product

# --- 1. بوابة دخول الإدارة ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_panel.admin_dashboard'))
        logout_user()
        
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username, role='admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('⚠️ فشل التحقق السيادي: بيانات الإدارة غير صحيحة.', 'danger')
            
    return render_template('admin_panel/login.html')

# --- 2. لوحة التحكم المركزية ---
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    return render_template('admin_panel/dashboard.html')

# --- 3. إدارة الموردين ---
@admin_bp.route('/suppliers')
@login_required
def admin_suppliers_management():
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    # هنا يمكنك جلب الموردين لعرضهم في الصفحة
    return render_template('admin_panel/admin_suppliers_management.html')

# --- 4. مراجعة المنتجات ---
@admin_bp.route('/product-review')
@login_required
def product_review():
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    return render_template('admin_panel/product_review.html')

# --- 5. تفاصيل المنتج ---
@admin_bp.route('/product-detail/<int:id>')
@login_required
def product_detail(id):
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    return render_template('admin_panel/product_detail.html')

# --- 6. المحفظة والمالية ---
@admin_bp.route('/wallets')
@login_required
def wallets():
    if current_user.role != 'admin':
        return redirect(url_for('admin_panel.admin_login'))
    return render_template('admin_panel/wallets.html')

# --- 7. تسجيل الخروج ---
@admin_bp.route('/logout')
def admin_logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))
