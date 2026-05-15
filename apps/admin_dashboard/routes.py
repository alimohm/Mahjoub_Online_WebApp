# coding: utf-8
# 🖥️ وحدة القيادة المركزية - محجوب أونلاين 2026

from flask import render_template
from flask_login import login_required # لحماية اللوحة من المتطفلين
from . import admin_dashboard 

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
@login_required # لا يمكن الدخول هنا إلا بعد المرور بصفحة /auth/login
def dashboard():
    """
    عرض مركز المراقبة الرئيسي.
    يتم حقن dashboard_content.html داخل admin_base.html
    """
    return render_template('admin/dashboard_content.html')

@admin_dashboard.route('/suppliers/list')
@login_required
def list_suppliers():
    """
    عرض سجل الموردين.
    تأكد أن الملف موجود في: apps/admin_dashboard/templates/admin/list_suppliers.html
    """
    # هنا سنقوم لاحقاً بجلب البيانات من قاعدة البيانات db.session.query(Supplier)
    return render_template('admin/list_suppliers.html')
