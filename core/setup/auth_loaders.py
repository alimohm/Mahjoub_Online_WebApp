# core/setup/auth_loaders.py
from core.extensions import login_manager
# نستخدم الاستيراد داخل الدالة أو من النقطة المركزية لتجنب الدوائر المغلقة
from core.models import User, Supplier

@login_manager.user_loader
def load_user(user_id):
    """
    محرك استعادة الهوية السيادي:
    يتحقق من الهوية في ترسانة المدراء أولاً، ثم الموردين.
    """
    
    # حماية ضد القيم الفارغة أو غير الصالحة
    if not user_id or user_id == 'None':
        return None
    
    try:
        uid = int(user_id)
        
        # 1. فحص جدول المستخدمين (القيادة المركزية)
        user = User.query.get(uid)
        if user:
            # إضافة وسم لتمييز نوع المستخدم برمجياً إذا احتجنا لاحقاً
            user.is_admin_account = True 
            return user
            
        # 2. فحص جدول الموردين (القاعدة التجارية)
        supplier = Supplier.query.get(uid)
        if supplier:
            supplier.is_admin_account = False
            return supplier
            
    except Exception as e:
        # طباعة الخطأ في سجلات Railway للتشخيص الدقيق
        print(f"⚠️ خطأ في محرك استعادة الهوية: {e}")
        return None

    return None
