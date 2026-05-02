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
