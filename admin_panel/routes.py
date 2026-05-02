from flask import render_template
from flask_login import login_required, current_user
from . import admin_bp
from core.models.user import User
# استيراد موديلات الموردين والطلبات (تأكد من وجود هذه الموديلات في core)
# from core.models.business import Supplier, Order 

@admin_bp.route('/dashboard')
@login_required  # حماية السيادة: الدخول للقائد فقط
def admin_dashboard():
    """
    لوحة التحكم المركزية لإدارة الخط التجاري في اليمن
    """
    # هنا نقوم بجلب إحصائيات حقيقية لعرضها في الواجهة
    # مثال: إحصائيات الموردين في (الخوخة، عدن، المخا، وحيس)
    stats = {
        'total_suppliers': 0, # سيتم جلبها من قاعدة البيانات لاحقاً
        'active_orders': 0,
        'cities_covered': ['الخوخة', 'عدن', 'المخا', 'حيس']
    }
    
    # تمرير اسم القائد (علي) والإحصائيات إلى صفحة dashboard.html
    return render_template(
        'dashboard.html', 
        title="برج الرقابة المركزية",
        admin_name=current_user.username,
        stats=stats
    )
from flask import render_template
from flask_login import login_required
from . import admin_bp

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    # جلب البيانات الحقيقية من قاعدة البيانات
    # هذه المتغيرات يجب أن تطابق الأسماء في ملف HTML الخاص بك
    context = {
        'orders_count': "1,250",       # إجمالي المبيعات
        's_count': "48",              # شركاء الترسانة (الموردين)
        'total_balance': "15.5K",      # السيولة المركزية
        'p_count': "12",               # طلبات قيد التدقيق
        'transactions': [              # سجل العمليات (نموذج بيانات)
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
    
    return render_template('dashboard.html', **context)
