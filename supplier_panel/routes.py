from flask import Blueprint
from flask_login import login_required
from .auth_logic import SupplierController

# تعريف البلوبرينت الخاص بالموردين
# تم التأكيد على template_folder لضمان قراءة المجلد الفرعي supplier_panel داخل templates
supplier_bp = Blueprint(
    'supplier_panel', 
    __name__, 
    template_folder='templates'
)

# إنشاء نسخة من المتحكم (Controller)
auth_controller = SupplierController()

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    """مسار تسجيل دخول الموردين - يربط مع supplier_panel/supplier_login.html"""
    return auth_controller.login_logic()

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    """
    مسار لوحة تحكم المورد (شريك النجاح).
    تمت إضافة @login_required لضمان أمان البيانات والحوكمة الرقمية.
    """
    return auth_controller.dashboard_logic()

@supplier_bp.route('/logout')
@login_required
def logout():
    """مسار تسجيل الخروج الآمن"""
    return auth_controller.logout_logic()
