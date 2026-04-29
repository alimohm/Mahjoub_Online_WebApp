from flask import Blueprint
from flask_login import login_required
from .auth_logic import SupplierAuthLogic

# تعريف البلوبرينت الخاص بالموردين
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    # استدعاء منطق تسجيل الدخول
    return SupplierAuthLogic.login_process()

@supplier_bp.route('/dashboard')
@login_requiredfrom flask import Blueprint
from flask_login import login_required
from .supplier_controller import SupplierController

# تعريف البلوبرينت الخاص بالموردين مع تحديد مجلد القوالب
supplier_bp = Blueprint('supplier_panel', __name__, template_folder='templates')

# إنشاء نسخة من المتحكم الخاص بالموردين
# هذا يضمن توافق الدوال مع كلاس SupplierController
supplier_controller = SupplierController()

# --- مسارات بوابة دخول الموردين ---

@supplier_bp.route('/login', methods=['GET', 'POST'])
def supplier_login():
    """بوابة دخول شركاء النجاح (الموردين)"""
    return supplier_controller.login_logic()

@supplier_bp.route('/logout')
@login_required
def logout():
    """تسجيل خروج المورد"""
    return supplier_controller.logout_logic()

# --- مسارات إدارة المنتجات والمخزون ---

@supplier_bp.route('/dashboard')
@login_required
def supplier_dashboard():
    """لوحة تحكم المورد لمتابعة المبيعات والطلبات"""
    return supplier_controller.dashboard_logic()

@supplier_bp.route('/my-products')
@login_required
def manage_products():
    """إدارة المنتجات الخاصة بالمورد"""
    return supplier_controller.products_logic()

@supplier_bp.route('/orders')
@login_required
def view_orders():
    """متابعة طلبات الزبائن الواردة للمورد"""
    return supplier_controller.orders_logic()

@supplier_bp.route('/account-settings')
@login_required
def settings():
    """تحديث بيانات المورد وربط الـ Webhooks"""
    return supplier_controller.settings_logic()
def supplier_dashboard():
    # استدعاء منطق لوحة التحكم
    return SupplierAuthLogic.dashboard_process()

@supplier_bp.route('/my-products')
@login_required
def my_products():
    # استدعاء منطق إدارة المنتجات
    return SupplierAuthLogic.products_list_process()

@supplier_bp.route('/logout')
@login_required
def supplier_logout():
    # استدعاء منطق تسجيل الخروج
    return SupplierAuthLogic.logout_process()
