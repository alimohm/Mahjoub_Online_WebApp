# admin_panel/routes.py
import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text

# الاستيراد الصحيح من الهيكلية الجديدة
from core.extensions import db 
from core.models.supplier import Supplier
from core.models.user import User

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي (علي محجوب فقط) ---
def is_admin_sovereign():
    """
    التحقق من أن المستخدم يمتلك رتبة 'admin' لضمان أمان مركز القيادة.
    """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. بوابة الدخول (The Gateway) ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 3. مركز القيادة (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('main.index'))
    
    try:
        # إحصائيات من الموديلات الجديدة
        # نستخدم حساب الموردين من جدول Supplier المخصص
        suppliers_count = Supplier.query.count()
        total_users = User.query.count()
        
        # حماية إضافية لجدول الطلبات (Orders)
        try:
            from core.models.business import Order
            total_orders = Order.query.count()
        except Exception:
            total_orders = 0

        stats = {
            'suppliers_count': suppliers_count,
            'orders_count': total_orders,
            'users_count': total_users,
            'pending_withdrawals': 0 
        }
        
        return render_template('dashboard.html', **stats)
        
    except Exception as e:
        print(f"⚠️ Dashboard Crash Avoided: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, pending_withdrawals=0)

# --- 4. إدارة الموردين (Supplier Management) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """
    عرض الموردين النشطين في المنظومة (مثل موردين المعاز والإلكترونيات).
    """
    if not is_admin_sovereign(): 
        return redirect(url_for('main.index'))
    
    try:
        # جلب الموردين من الموديل السيادي الجديد
        suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
        return render_template('manage_suppliers.html', suppliers=suppliers)
    except Exception as e:
        flash(f"خلل في الوصول للموردين: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

# --- 5. إنهاء الجلسة (Logout) ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم الخروج الآمن من نظام الإدارة", "info")
    return redirect(url_for('admin.login'))

# --- 6. إضافة مورد جديد (Expanding the Network) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        try:
            # منطق إضافة المورد (يمكن توسيعه لاحقاً لاستقبال البيانات من Form)
            flash("بروتوكول إضافة الموردين قيد التفعيل حالياً", "success")
            return redirect(url_for('admin.manage_suppliers'))
        except Exception as e:
            flash(f"فشل في إضافة المورد: {str(e)}", "danger")

    return render_template('add_supplier.html')
