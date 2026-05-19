# coding: utf-8
# 🛡️ مركز القيادة والتحكم - محرك الحوكمة المالية 2026

from flask import Blueprint, render_template
from flask_login import login_required, current_user
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet
# استدعاء موديلات الطلبات إذا وجدت في مشروعك
# from apps.models.order_db import Order 

admin_dashboard = Blueprint('admin_dashboard', __name__, template_folder='templates')

@admin_dashboard.route('/admin/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    try:
        # 1. إحصائيات الموردين (الشركاء)
        total_suppliers = Supplier.query.count()
        
        # 2. إحصائيات المحافظ (السيولة المالية)
        # جلب إجمالي المحافظ لضمان التفاعل مع الأرصدة
        total_wallets = Wallet.query.count()
        
        # 3. إحصائيات الطلبات (تم تعيينها افتراضياً لعدم وجود الموديل حالياً)
        active_orders = 0 
        
        # 4. بناء كائن الإحصائيات (Stats) الذي يتوقعه القالب
        stats = {
            'total_suppliers': total_suppliers,
            'active_orders': active_orders,
            'system_health': '100%',
            'server_status': 'Online'
        }
        
        # 5. عرض الصفحة مع تمرير البيانات
        return render_template('admin/dashboard.html', 
                               owner=current_user, 
                               stats=stats)
        
    except Exception as e:
        # في حال حدوث عطل برمجي، نمنع انهيار الصفحة ونعرض رسالة خطأ
        print(f"DASHBOARD ERROR: {str(e)}")
        # نمرر إحصائيات صفرية لمنع حدوث خطأ في القالب
        return render_template('admin/dashboard.html', 
                               owner=current_user, 
                               stats={'total_suppliers': 0, 'active_orders': 0, 'system_health': 'Error', 'server_status': 'Offline'})

# مسارات إضافية للوحة التحكم (مثل قائمة الموردين)
@admin_dashboard.route('/admin/suppliers', methods=['GET'])
@login_required
def list_suppliers():
    suppliers = Supplier.query.all()
    return render_template('admin/suppliers.html', suppliers=suppliers)
