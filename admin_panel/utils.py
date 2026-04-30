from functools import wraps
from flask import abort
from flask_login import current_user

def admin_required(f):
    """
    مُزيّن (Decorator) لضمان أن المستخدم المسجل لديه صلاحيات المسؤول (Admin).
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # التحقق من أن المستخدم مسجل دخول ولديه رتبة admin
        if not current_user.is_authenticated or getattr(current_user, 'role', None) != 'admin':
            # إذا لم يكن مسؤولاً، يتم إرجاع خطأ 403 (غير مصرح)
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
