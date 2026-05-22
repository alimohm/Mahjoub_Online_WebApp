# coding: utf-8
# 🚀 محرك المسارات الخلفي للوحة التحكم - منصة محجوب أونلاين 2026

from flask import render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import func
from . import admin_dashboard_bp

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    try:
        from apps.extensions import db
        from apps.models.wallet_db import SupplierWallet
        
        # 💵 جلب الحسابات المالية الحية من الخزائن مباشرة لتغذية الكروت
        totals = db.session.query(
            func.coalesce(func.sum(SupplierWallet.yer_total + SupplierWallet.yer_pending), 0).label('total_yer'),
            func.coalesce(func.sum(SupplierWallet.sar_total + SupplierWallet.sar_pending), 0).label('total_sar'),
            func.coalesce(func.sum(SupplierWallet.usd_total + SupplierWallet.usd_pending), 0).label('total_usd')
        ).filter(SupplierWallet.status == 'نشطة').first()
        
        # 🧠 هنا الذكاء: إذا كان الطلب قادماً من محرك الجافاسكريبت (Fetch)
        # نرسل له كود الكروت الصافي فقط بدون وراثة القالب الأب لمنع خطأ 405 أو التداخل
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return render_template('admin/dashboard_content.html', totals=totals, bootstrap_render=False)
            
        # إذا كان الدخول أول مرة (تحديث كامل للصفحة من المتصفح)، نرسل الصفحة شاملة الهيكل
        return render_template('admin/dashboard_content.html', totals=totals, bootstrap_render=True)
                               
    except Exception as e:
        fallback_totals = {'total_yer': 0.00, 'total_sar': 0.00, 'total_usd': 0.00}
        return render_template('admin/dashboard_content.html', totals=fallback_totals)


# 🏬 مسار جلب "سجل الموردين" كـ كود صافي ومجرد لحقنه عبر المحرك
@admin_dashboard_bp.route('/suppliers/list', methods=['GET'])
@login_required
def list_suppliers():
    try:
        from apps.models.supplier_db import Supplier
        suppliers_list = Supplier.query.order_by(Supplier.id.desc()).all()
        
        # يرجع جدول الموردين الصافي فقط بدون وسم extends وبدون القوائم الجانبية
        return render_template('admin/list_suppliers.html', suppliers=suppliers_list)
    except Exception as e:
        return f"<div class='alert alert-danger'>فشل استدعاء السجل برمجياً: {str(e)}</div>", 500


# 🛡️ مسار إعدادات السيادة
@admin_dashboard_bp.route('/settings/sovereignty', methods=['GET'])
@login_required
def system_settings():
    return render_template('admin/system_settings.html')
