# coding: utf-8
# 📊 وحدة القيادة المركزية الديناميكية - منصة محجوب أونلاين 2026

from flask import render_template, current_app, redirect, url_for
from flask_login import login_required, current_user 
import jinja2

# استيراد البلوبرينت الموحد لمنع تعذر العثور على الكائن أثناء الإقلاع
from . import admin_dashboard_blueprint 


@admin_dashboard_blueprint.route('/')
@admin_dashboard_blueprint.route('/dashboard')
@login_required # درع حماية النفاذ السيادي
def dashboard_home():
    """
    عرض مركز المراقبة الرئيسي بروابط وتطبيقات ديناميكية بالكامل.
    يتم قراءة محركات النظام (Micro-Engines) المسجلة في النواة وتمرير مساراتها تلقائياً.
    """
    stats = {
        'total_suppliers': 0,
        'active_orders': 0,
        'system_health': '100%',
        'server_status': 'Online'
    }

    # 🗺️ خريطة الروابط السيادية الديناميكية لمنع الـ BuildError مستقبلاً
    # تفحص النواة تلقائياً إذا كان التطبيق (البلوبرينت) مسجلاً أم لا، وتولد الرابط المناسب له
    dynamic_endpoints = {
        'add_supplier': None,
        'list_suppliers': url_for('admin_dashboard.list_suppliers')
    }

    # الفحص التلقائي لمحرك الموردين المعزول في النواة
    if 'admin_suppliers' in current_app.blueprints:
        # إذا تم تسجيل تطبيق الموردين، نربطه بدالته الجديدة لمنع التداخل والتعارض
        dynamic_endpoints['add_supplier'] = url_for('admin_suppliers.add_supplier_page')
    else:
        # حماية احتياطية في حال تم إلغاء تفعيل المحرك مؤقتاً لتجنب خطأ 500
        dynamic_endpoints['add_supplier'] = '#'

    # 💡 [مستقبلاً]: بمجرد بناء تطبيق جديد، مثلاً (apps.add_agent)، فقط أضف الفحص هنا دون لمس بقية المسارات:
    # if 'admin_agents' in current_app.blueprints:
    #     dynamic_endpoints['add_agent'] = url_for('admin_agents.add_agent_page')

    # محاولة رندرة القالب بالمسار المعزول، وإذا تعذر يتم البحث عنه في المسار المباشر منعا للانهيار
    try:
        return render_template(
            'admin/dashboard_content.html', 
            stats=stats, 
            owner=current_user, 
            endpoints=dynamic_endpoints
        )
    except jinja2.exceptions.TemplateNotFound:
        current_app.logger.warning("تنبيه: تم موازنة مسار القالب المعزول لـ dashboard_content")
        return render_template(
            'dashboard_content.html', 
            stats=stats, 
            owner=current_user, 
            endpoints=dynamic_endpoints
        )


@admin_dashboard_blueprint.route('/suppliers/list')
@login_required
def list_suppliers():
    """عرض سجل الموردين"""
    try:
        return render_template('admin/list_suppliers.html', owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('list_suppliers.html', owner=current_user)


@admin_dashboard_blueprint.route('/settings')
@login_required
def system_settings():
    """إعدادات المنصة السيادية"""
    try:
        return render_template('admin/settings.html', owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('settings.html', owner=current_user)
