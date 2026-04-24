from flask import Blueprint, render_template, request
from core.qumra_sync import qumra_manager  # استيراد المحرك اللحظي

# تعريف البلوبرنت
admin_bp = Blueprint('admin_panel', __name__, template_folder='templates')

# 1. لوحة التحكم (الرئيسية)
@admin_bp.route('/', strict_slashes=False)
def dashboard():
    # نقل الاستيراد إلى هنا يمنع الخطأ (Circular Import)
    from core.models import Supplier, Product
    try:
        suppliers_count = Supplier.query.count()
        products_count = Product.query.count()
        return render_template('dashboard.html', s_count=suppliers_count, p_count=products_count)
    except Exception:
        return render_template('dashboard.html', s_count=0, p_count=0)

# 2. عرض المنتجات اللحظي القادم من قمرة
@admin_bp.route('/sync_now', strict_slashes=False)
def sync_now():
    # جلب البيانات مباشرة من قمرة لعرضها في لوحة إدارتك
    live_products = qumra_manager.fetch_live_products(limit=15)
    return render_template('product_review.html', products=live_products)

# 3. عرض قائمة الموردين
@admin_bp.route('/suppliers', strict_slashes=False)
def list_suppliers():
    from core.models import Supplier
    suppliers = Supplier.query.all()
    return render_template('suppliers_list.html', suppliers=suppliers)
