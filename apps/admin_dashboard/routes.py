# apps/admin_dashboard/routes.py
from flask import render_template
from . import admin_dashboard_bp # الـ Blueprint الخاص بلوحة التحكم

@admin_dashboard_bp.route('/dashboard')
def dashboard():
    # لاحظ كيف نمرر البيانات بشكل منظم
    return render_template('admin/dashboard.html', active_page='dashboard')

@admin_dashboard_bp.route('/suppliers/add')
def add_supplier_route():
    return render_template('admin/add_supplier.html', active_page='add_supplier')
