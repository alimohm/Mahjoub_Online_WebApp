# coding: utf-8
from flask import Blueprint, render_template, abort
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier

# 🎯 الاسم المعرّف هنا هو المسؤول عن حل مشكلة BuildError
# يجب أن يكون مطابقاً تماماً للاسم المستخدم في url_for في admin_base.html
admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    مركز القيادة السيادي
    """
    try:
        # استعلامات آمنة ومستقلة
        total_suppliers = Supplier.query.count()
        
        stats = {
            'total_suppliers': total_suppliers,
            'active_orders': 0,
            'system_health': '100% مستقر'
        }
        
        return render_template('admin/dashboard_content.html', 
                               current_user=current_user, 
                               stats=stats)
    except Exception as e:
        print(f"Error loading dashboard: {e}")
        return "حدث خطأ في تحميل مركز القيادة", 500

@admin_dashboard.route('/settings', methods=['GET'])
@login_required
def system_settings():
    """
    مسار إعدادات السيادة
    """
    return render_template('admin/settings.html', current_user=current_user)

@admin_dashboard.route('/suppliers/list', methods=['GET'])
@login_required
def list_suppliers():
    """
    عرض قائمة الموردين
    """
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
