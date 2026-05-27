# coding: utf-8
# 📊 لوحة التحكم الإدارية - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request
from flask_login import login_required
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.utils.security import cipher_suite

# تعريف الـ Blueprint مع تحديد مجلد القوالب المحلي
# هذا المسار يضمن أن Flask يبحث عن القوالب في: apps/admin_dashboard/templates/
admin_dashboard = Blueprint(
    'admin_dashboard', 
    __name__, 
    template_folder='templates'
)

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard():
    """
    تحميل بيانات لوحة التحكم مع معالجة آمنة للقيم المشفرة والأعمدة
    """
    try:
        # 1. إحصائيات الموردين
        total_suppliers = Supplier.query.count()
        
        # 2. حساب الأرصدة 
        # نستخدم الدالة الآمنة لفك التشفير أو التحويل المباشر لتجنب الانهيار
        wallets = SupplierWallet.query.all()
        
        # جمع الأرصدة مع التعامل مع القيم المشفرة (تنسيق Fernet)
        total_sar_balance = sum([cipher_suite.decrypt_to_float(w._sar_total) for w in wallets])
        total_yer_balance = sum([cipher_suite.decrypt_to_float(w._yer_total) for w in wallets])
        
        # حساب الإجمالي
        total_balance = total_sar_balance + (total_yer_balance / 3.75) 
        
        # 3. آخر 5 عمليات (ترتيب حسب التاريخ)
        recent_activities = WalletTransaction.query.order_by(
            WalletTransaction.created_at.desc()
        ).limit(5).all()
        
        # 4. التسويات المعلقة
        pending_settlements = WalletTransaction.query.filter_by(status='معلقة').count()

        # إرجاع القالب من المسار: apps/admin_dashboard/templates/admin/dashboard_content.html
        return render_template(
            'admin/dashboard_content.html',
            total_suppliers=total_suppliers,
            total_balance=f"{total_balance:,.2f}",
            pending_settlements=pending_settlements,
            recent_activities=recent_activities
        )
        
    except Exception as e:
        # تسجيل الخطأ في السجلات للتشخيص
        print(f"❌ Error loading dashboard: {str(e)}")
        
        # رسالة واجهة المستخدم في حال فشل التحميل
        return f"""
        <div style="text-align:center; margin-top:50px; font-family:sans-serif; direction:rtl;">
            <h2>حدث خطأ أثناء تحميل لوحة التحكم</h2>
            <p>يرجى التأكد من هيكل البيانات: {str(e)}</p>
            <a href="/admin/dashboard" style="padding:10px; background:#632C8F; color:white; text-decoration:none; border-radius:5px;">حاول مجدداً</a>
        </div>
        """, 500
