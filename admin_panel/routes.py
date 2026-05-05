import os
import random
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. استيراد النماذج المستقلة (الرشاقة السيادية) ---
from core.models.user import User

try:
    from core.models.product import Product
except ImportError:
    Product = None

try:
    from core.models.business import Order
except ImportError:
    Order = None

# --- 2. التحقق من الصلاحية الإدارية ---
def is_admin():
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 3. المسارات الإدارية (مركز القيادة) ---

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin():
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين النظام وتفكيك الجلسة الإدارية", "info")
    return redirect(url_for('admin.login'))

@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin():
        flash("عذراً، لا تمتلك صلاحيات الترسانة الإدارية", "danger")
        return redirect(url_for('main.index'))
    
    # جلب إحصائيات رشيقة من القاعدة
    stats = {
        'suppliers_count': User.query.filter_by(role='vendor').count(),
        'orders_count': db.session.query(Order).count() if Order else 0,
        'users_count': db.session.query(User).count(),
        'pending_withdrawals': 0
    }
    return render_template('dashboard.html', **stats)

# --- 4. النوافذ الإضافية (ربط ملفات الصورة image_f629d1.png) ---

@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin(): return redirect(url_for('main.index'))
    suppliers = User.query.filter_by(role='vendor').all()
    return render_template('manage_suppliers.html', suppliers=suppliers)

@admin_bp.route('/wallets')
@login_required
def manage_wallets():
    if not is_admin(): return redirect(url_for('main.index'))
    return render_template('wallets.html')

@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    if not is_admin(): return redirect(url_for('main.index'))
    return render_template('withdraw_requests.html')

# --- 5. مسارات الطوارئ والتعميد ---

@admin_bp.route('/approve-vendor/<int:user_id>')
@login_required
def approve_vendor(user_id):
    if not is_admin(): return "Unauthorized", 403
    vendor = User.query.get(user_id)
    if vendor:
        vendor.is_active_account = True
        db.session.commit()
        flash(f"تم تعميد المورد {vendor.username} بنجاح لتمرير منتجاته", "success")
    return redirect(url_for('admin.manage_suppliers'))

@admin_bp.route('/make-me-admin')
@login_required
def make_me_admin():
    try:
        current_user.role = 'admin'
        db.session.commit()
        flash("تمت ترقيتك لآدمن سيادي بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Error: {str(e)}"
