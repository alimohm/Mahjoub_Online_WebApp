from flask import render_template, redirect, url_for, flash, request
from flask_login import login_required, logout_user, current_user
from . import admin_bp
from .auth import handle_admin_login
# من المفترض استيراد الموديلات هنا لاحقاً (مثل User, Supplier, Order)

@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    """معالجة تسجيل دخول السلطة العليا"""
    if current_user.is_authenticated:
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """مركز المراقبة والتحكم المركزي"""
    # هذه البيانات سيتم جلبها من قاعدة البيانات لاحقاً
    stats = {
        'orders_count': "1,250", 
        'suppliers_count': "48",
        'total_balance': "15,500",
        'pending_requests': "12",
        'active_users': "320"
    }
    return render_template('dashboard.html', **stats)

@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    """حوكمة الموردين المعتمدين"""
    # سيتم ربطها بجدول الموردين في قاعدة البيانات
    return render_template('manage_suppliers.html')

@admin_bp.route('/financial-engineering')
@login_required
def financial_reports():
    """تقارير الهندسة المالية والأرباح"""
    return render_template('financial_reports.html')

@admin_bp.route('/system-settings')
@login_required
def system_settings():
    """إعدادات السيادة والتحكم بالنظام"""
    return render_template('settings.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """إنهاء الجلسة الآمنة والعودة للشرنقة"""
    logout_user()
    flash('تم إنهاء الجلسة الآمنة بنجاح. ننتظر عودتك يا قائد.', 'info')
    return redirect(url_for('admin.admin_login'))
