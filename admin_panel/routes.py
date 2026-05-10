# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user, current_user
from datetime import datetime
from . import admin_bp

# الاستيراد من النواة لجلب البيانات الإحصائية فقط
from core.models.user import User
from core.models.supplier import Supplier

# --- 1. بروتوكول التحقق السيادي (للإحصائيات فقط) ---
def is_admin_sovereign():
    """ يضمن أن القائد علي (Admin) فقط يرى الإحصائيات """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. مركز القيادة الإحصائي (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    # جلب الأرقام الحية لنبض النظام
    stats = {
        'users_count': User.query.count() if User else 0,
        'suppliers_count': Supplier.query.count() if Supplier else 0,
        'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    
    # محاولة جلب الطلبات إذا كان الموديل موجوداً
    try:
        from core.models.business import Order
        stats['orders_count'] = Order.query.count()
    except ImportError:
        stats['orders_count'] = "قيد التطوير"

    return render_template('dashboard.html', **stats)

# --- 3. عرض واجهة إدارة الموردين (القشرة الخارجية فقط) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """ 
    هذا الرابط يفتح الصفحة فقط. 
    العمليات (البحث، الحذف، التعديل) تتم عبر محرك manage_suppliers.py 
    """
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 4. إنهاء الجلسة السيادية ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تأمين الخروج من مركز القيادة بنجاح.", "info")
    return redirect(url_for('admin.login'))
