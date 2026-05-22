from flask import render_template, request, jsonify
from datetime import datetime
from . import admin_dashboard_bp # افترضت أنك تستخدم Blueprint باسم admin_dashboard_bp
from ..models import User, Supplier, Order # افترض استيراد النماذج من مشروعك

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
def dashboard():
    # 1. تجهيز البيانات (هنا تربط الدوال بـ DB)
    stats = {
        'users_count': User.query.count(),
        'suppliers_count': Supplier.query.count(),
        'orders_count': Order.query.count(),
        'total_yer': '25,000,000', # استبدل هذه القيم بـ Database Queries
        'total_sar': '50,000',
        'total_usd': '12,000',
        'now': datetime.now()
    }

    # 2. إذا كان الطلب من الرابط الجانبي (AJAX) - نرسل المحتوى فقط
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/dashboard_content.html', **stats)
    
    # 3. إذا كان دخولاً مباشراً للصفحة - نرسل الهيكل الكامل
    return render_template('admin/admin_base.html', **stats)

# مثال إضافي لتنظيم المسارات
@admin_dashboard_bp.route('/add_supplier', methods=['GET'])
def add_supplier():
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/add_supplier_form.html')
    return render_template('admin/admin_base.html')
