from flask import Blueprint
from .auth_logic import SupplierController

# تعريف البلوبرينت الخاص بالموردين مع تحديد مسار القوالب
# لاحظ استخدام المسار الكامل ليتوافق مع هيكلية المجلدات التي ذكرتها
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates'
)

# إنشاء نسخة من المتحكم
auth_controller = SupplierController()

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    """مسار تسجيل دخول الموردين"""
    return auth_controller.login_logic()

@supplier_bp.route('/dashboard')
def supplier_dashboard():
    """مسار لوحة تحكم المورد (شريك النجاح)"""
    return auth_controller.dashboard_logic()

@supplier_bp.route('/logout')
def logout():
    """مسار تسجيل الخروج"""
    return auth_controller.logout_logic()
