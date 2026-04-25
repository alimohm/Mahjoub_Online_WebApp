from functools import wraps
from flask import redirect, url_for, request
from flask_login import current_user

def sovereign_approval_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 1. التحقق من تسجيل الدخول أولاً
        if not current_user.is_authenticated:
            return redirect(url_for('supplier_panel.login'))

        # 2. التحقق من حالة "التعميد" (is_approved)
        # ملاحظة: نتحقق من وجود الخاصية أولاً لتجنب الأخطاء
        is_approved = getattr(current_user, 'is_approved', False)
        
        if not is_approved:
            # إذا كان المورد غير معتمد، يتم توجيهه حصراً لصفحة الانتظار
            # التحقق من request.endpoint يمنع إعادة التوجيه اللانهائي
            if request.endpoint != 'supplier_panel.waiting_room':
                return redirect(url_for('supplier_panel.waiting_room'))
        
        return f(*args, **kwargs)
    return decorated_function
