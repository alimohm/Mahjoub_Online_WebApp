# coding: utf-8
# 📊 وحدة القيادة المركزية - محجوب أونلاين 2026

from flask import render_template
from flask_login import login_required, current_user 

# استيراد البلوبرينت الموحد لمنع تعذر العثور على الكائن أثناء الإقلاع
from . import admin_dashboard_blueprint 


@admin_dashboard_blueprint.route('/')
@admin_dashboard_blueprint.route('/dashboard')
@login_required # درع حماية النفاذ السيادي
def dashboard_home():
    """
    عرض مركز المراقبة الرئيسي.
    يتم حقن dashboard_content.html داخل الإطار الملكي admin_base.html
    """
    # إحصائيات أولية للمنصة لضمان الإقلاع السريع المستقر
    stats = {
        'total_suppliers': 0,
        'active_orders': 0,
        'system_health': '100%',
        'server_status': 'Online'
    }
    
    # تمرير البيانات للقالب الملكي
    return render_template('admin/dashboard_content.html', stats=stats, owner=current_user)


@admin_dashboard_blueprint.route('/suppliers/list')
@login_required
def list_suppliers():
    """عرض سجل الموردين"""
    return render_template('admin/list_suppliers.html', owner=current_user)


@admin_dashboard_blueprint.route('/settings')
@login_required
def system_settings():
    """إعدادات المنصة السيادية"""
    return render_template('admin/settings.html', owner=current_user)
