# coding: utf-8
# 📊 لوحة التحكم الإدارية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template
from flask_login import login_required
from apps.extensions import db # استيراد db فقط من مكان آمن
from sqlalchemy import func

# تعريف الـ Blueprint
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    تحميل بيانات لوحة التحكم مع تحصين كامل ضد انهيار قاعدة البيانات
    """
    # 1. الاستيراد المحلي (Lazy Import) - هنا نكسر الحلقة الدائرية
    from apps.models.supplier_db import Supplier
    from apps.models.wallet_db import SupplierWallet, WalletTransaction
    
    # قيم افتراضية لضمان عدم انهيار القالب (Template)
    stats = {
        'total_suppliers': 0,
        'total_balance': "0.00",
        'pending_settlements': 0,
        'recent_activities': []
    }

    try:
        # إحصائيات الموردين
        stats['total_suppliers'] = Supplier.query.count()
        
        # حساب الأرصدة
        sar_sum = db.session.query(func.sum(SupplierWallet.sar_total)).scalar() or 0
        yer_sum = db.session.query(func.sum(SupplierWallet.yer_total)).scalar() or 0
        
        total_balance = sar_sum + (yer_sum / 3.75)
        stats['total_balance'] = f"{total_balance:,.2f}"

        # آخر 5 عمليات
        stats['recent_activities'] = WalletTransaction.query.order_by(
            WalletTransaction.id.desc()
        ).limit(5).all()
        
        # التسويات المعلقة
        stats['pending_settlements'] = WalletTransaction.query.filter_by(status='معلقة').count()

        return render_template('admin/dashboard_content.html', **stats)
        
    except Exception as e:
        print(f"❌ Critical Dashboard Error: {str(e)}")
        # في حال حدوث خطأ، نمرر القيم الافتراضية لعرض لوحة فارغة بدلاً من الانهيار
        return render_template('admin/dashboard_content.html', **stats)
