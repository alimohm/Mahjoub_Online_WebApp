from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user
from core.models import User # الاستيراد من النواة المركزية

def sovereign_approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. التحقق من تسجيل الدخول (خط الدفاع الأول)
        if not current_user.is_authenticated:
            return redirect(url_for('supplier_panel.login'))

        # 2. كسر الكاش الرقمي: استعلام مباشر عن حالة المورد السيادي
        # نصل للمورد عبر البروفايل المرتبط بـ User
        user = User.query.get(current_user.id)
        supplier = user.supplier_profile if user else None
        
        # 3. فحص الاعتماد (is_approved) والحالة (status)
        if not supplier or not supplier.is_approved or supplier.status != 'active':
            # منع التكرار اللانهائي: إذا لم يكن في صفحة الانتظار، أرسله إليها
            if request.endpoint != 'supplier_panel.waiting_room':
                return redirect(url_for('supplier_panel.waiting_room'))
        
        # 4. إذا كان المورد معتمداً وحالته نشطة، يمر بسلام
        return f(*args, **kwargs)
        
    return decorated_function
