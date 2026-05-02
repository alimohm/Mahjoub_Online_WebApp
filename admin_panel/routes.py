from flask import render_template
from flask_login import login_required, current_user
from . import admin_bp
# تأكد من استيراد الموديلات عند تفعيلها في قاعدة البيانات
# from core.models.business import Supplier, Order 

@admin_bp.route('/dashboard')
@login_required  # حماية السيادة: الوصول للقائد فقط
def admin_dashboard():
    """
    لوحة التحكم المركزية لإدارة الخط التجاري في اليمن (محجوب أونلاين)
    """
    
    # تجهيز البيانات لتتوافق مع تصميم dashboard.html
    # ملاحظة: يمكنك لاحقاً استبدال القيم النصية بطلبات Query من قاعدة البيانات
    context = {
        'orders_count': "1,250",       # إجمالي المبيعات (تظهر في البطاقة الأولى)
        's_count': "48",              # شركاء الترسانة - الموردين
        'total_balance': "15,500",     # السيولة المركزية بالدولار
        'p_count': "12",               # طلبات قيد التدقيق
        'admin_name': current_user.username, # عرض اسمك (علي) في الترحيب
        
        # بيانات العمليات السيادية للجدول
        'transactions': [
            {
                'supplier_name': 'مورد عدن المركزي',
                'type': 'توريد بضائع',
                'amount': 2500,
                'date': '2026-05-02',
                'status': 'مكتمل'
            },
            {
                'supplier_name': 'شركة المخا للاستيراد',
                'type': 'سحب سيولة',
                'amount': -450,
                'date': '2026-05-01',
                'status': 'قيد التدقيق'
            }
        ]
    }
    
    # تمرير البيانات كمتغيرات مستقلة باستخدام **context
    return render_template('dashboard.html', **context)
