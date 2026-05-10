# admin_panel/auth_logic.py
from core.models.user import User
from flask_login import login_user

class AdminAuthLogic:
    @staticmethod
    def authenticate_admin(username, password):
        """المنطق السيادي للتحقق من هوية المدير"""
        user = User.query.filter_by(username=username).first()
        
        if not user:
            return False, "⚠️ عذراً، هذا المستخدم غير مسجل في النظام.", None
            
        if not user.check_password(password):
            return False, "❌ كلمة المرور غير صحيحة، حاول مجدداً.", None
            
        if getattr(user, 'role', '').lower() != 'admin':
            return False, "🚫 الوصول مرفوض: الحساب لا يملك صلاحيات إدارية.", None

        if not getattr(user, 'is_active_account', True):
            return False, "🔒 الحساب موقوف حالياً، يرجى مراجعة الدعم.", None
            
        # إذا اجتاز كل الاختبارات
        login_user(user)
        return True, "تم فتح بوابة القيادة بنجاح.", user
