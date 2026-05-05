import os
import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. استيراد النماذج (نظام الوحدات المستقلة لضمان الرشاقة) ---
from core.models.user import User

try:
    from core.models.product import Product
except ImportError:
    Product = None

try:
    from core.models.business import Order
except ImportError:
    Order = None

# --- 2. وظائف التحقق السيادي ---
def check_admin_privilege():
    """التأكد من أن المستخدم الحالي هو علي محجوب أو آدمن معتمد"""
    if not current_user.is_authenticated or getattr(current_user, 'role', '').lower() != 'admin':
        return False
    return True

# --- 3. إدارة الجلسة والمصادقة ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين النظام وتفكيك الجلسة الإدارية بنجاح", "info")
    return redirect(url_for('admin.login'))

# --- 4. لوحة التحكم المركزية (مركز المراقبة) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not check_admin_privilege():
        flash("تنبيه: محاولة وصول غير مصرح بها للترسانة الإدارية", "danger")
        return redirect(url_for('main.index'))
    
    stats = {
        'suppliers_count': User.query.filter_by(role='vendor').count(),
        'pending_withdrawals': 0, # سيتم ربطه بموديل السحب لاحقاً
        'orders_count': db.session.query(Order).count() if Order else 0,
        'users_count': db.session.query(User).count()
    }
    return render_template('dashboard.html', **stats)

# --- 5. حوكمة الموردين (Manage Suppliers) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not check_admin_privilege(): return redirect(url_for('main.index'))
    
    # جلب كافة الموردين لعرضهم في نافذة manage_suppliers.html
    suppliers = User.query.filter_by(role='vendor').all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

@admin_bp.route('/approve-vendor/<int:user_id>')
@login_required
def approve_vendor(user_id):
    """تعميد المورد لتفعيل تمرير منتجاته إلى منصة قمرة"""
    if not check_admin_privilege(): return "Unauthorized", 403
    
    vendor = User.query.get(user_id)
    if vendor:
        vendor.is_active_account = True
        db.session.commit()
        flash(f"تم تعميد المورد {vendor.username} بنجاح كشريك سيادي", "success")
    return redirect(url_for('admin.manage_suppliers'))

# --- 6. هندسة المحافظ والرقابة المالية (Wallets) ---
@admin_bp.route('/wallets')
@login_required
def manage_wallets():
    if not check_admin_privilege(): return redirect(url_for('main.index'))
    
    # عرض المحافظ بالعملات الثلاث (YER, SAR, USD)
    # ملاحظة: سنقوم بربطها بموديل Wallet المستقل في الخطوة القادمة لضمان الرشاقة
    return render_template('wallets.html')

# --- 7. طلبات السحب (Withdraw Requests) ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    if not check_admin_privilege(): return redirect(url_for('main.index'))
    return render_template('withdraw_requests.html')

# --- 8. مسار الطوارئ (Admin Fixer) ---
@admin_bp.route('/make-me-admin')
@login_required
def make_me_admin():
    try:
        current_user.role = 'admin'
        db.session.commit()
        flash("بروتوكول الترقية اكتمل: أنت الآن الآدمن السيادي", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"
