# core/setup/auth_loaders.py
from core.extensions import login_manager
import logging

logger = logging.getLogger(__name__)

@login_manager.user_loader
def load_user(user_id):
    """
    محرك استعادة الهوية السيادي:
    يتحقق من الهوية في ترسانة المدراء أولاً، ثم الموردين.
    """
    
    if not user_id or user_id == 'None':
        return None
    
    # استيراد محلي لتجنب الدوائر المغلقة (Circular Import)
    from core.models.user import User
    from core.models.supplier import Supplier
    
    try:
        uid = int(user_id)
        
        # 1. فحص جدول المستخدمين (القيادة المركزية)
        # ملاحظة: إذا استمر الخطأ هنا، فهذا يؤكد ضرورة تشغيل init_db.py فوراً
        user = User.query.get(uid)
        if user:
            user.is_admin_account = True 
            return user
            
        # 2. فحص جدول الموردين (القاعدة التجارية)
        supplier = Supplier.query.get(uid)
        if supplier:
            supplier.is_admin_account = False
            return supplier
            
    except Exception as e:
        # تسجيل الخطأ في Railway للتشخيص
        logger.error(f"⚠️ عطل في رادار الهوية: {str(e)}")
        return None

    return None
