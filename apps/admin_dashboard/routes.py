# coding: utf-8
# 📂 apps/admin_dashboard/routes.py - لوحة التحكم السيادية (مُفعلة بالكامل)

from flask import Blueprint, render_template, abort, session
from flask_login import login_required, current_user
from apps.extensions import db
from sqlalchemy import func
from datetime import datetime

# استيراد النماذج المالية والسيادية
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.before_request
@login_required
def make_session_permanent():
    session.permanent = True
    session.modified = True 

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard():
    # 🛡️ حماية سيادية: التحقق من الصلاحيات
    if current_user.role not in ['Owner', 'Admin']:
        abort(403)

    try:
        # 1. إحصائيات الموردين
        total_suppliers = Supplier.query.count()
        
        # 2. حساب إجمالي الأرصدة المركزية من كافة محافظ الموردين
        # نستخدم func.sum لجلب القيم من قاعدة البيانات مباشرة
        balances = db.session.query(
            func.sum(SupplierWallet.balance_sar),
            func.sum(SupplierWallet.balance_yer),
            func.sum(SupplierWallet.balance_usd)
        ).first()

        # 3. جلب آخر 10 عمليات مالية حدثت في النظام للرقابة الفورية
        recent_transactions = WalletTransaction.query\
            .order_by(WalletTransaction.created_at.desc())\
            .limit(10).all()
        
        context = {
            'total_suppliers': total_suppliers,
            'total_balance_sar': float(balances[0] or 0),
            'total_balance_yer': float(balances[1] or 0),
            'total_balance_usd': float(balances[2] or 0),
            'recent_transactions': recent_transactions,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            'user_name': current_user.username,
            'store_name': 'محجوب أونلاين'
        }
        
        return render_template('admin/dashboard_content.html', **context)
        
    except Exception as e:
        # تسجيل الخطأ تقنياً وإظهاره بشكل مبسط
        print(f"🚨 Dashboard Error: {str(e)}")
        return f"🚨 عطل في المحرك المالي: {str(e)}", 500

@admin_dashboard.route('/system_logs', methods=['GET'])
@login_required
def system_logs():
    if current_user.role != 'Owner':
        abort(403)
    return "سجل الأحداث السيادي - قيد المراقبة"
