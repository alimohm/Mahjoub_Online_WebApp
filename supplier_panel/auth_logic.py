from core.models import User, Supplier
from werkzeug.security import check_password_hash

def verify_supplier_credentials(username, password):
    # 1. البحث عن المستخدم في الجدول الموحد
    user = User.query.filter_by(username=username, role='supplier').first()
    
    if not user:
        return "بيانات الدخول غير صحيحة أو الحساب ليس للموردين.", "danger", None
    
    # 2. التحقق من كلمة المرور
    if not check_password_hash(user.password, password):
        return "كلمة المرور غير صحيحة.", "danger", None
    
    # 3. التحقق من حالة الاعتماد السيادي (هل المورد مفعل؟)
    if user.supplier_profile and not user.supplier_profile.is_approved:
        return "حسابك قيد المراجعة السيادية، يرجى الانتظار.", "warning", user

    return "تم التحقق بنجاح.", "success", user
