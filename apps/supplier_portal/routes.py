from flask import Blueprint

supplier_bp = Blueprint('supplier_portal', __name__)

@supplier_bp.route('/supplier/dashboard')
def supplier_dashboard():
    return "<h1 style='color:#3D0066; background:#0A0A0A; text-align:center; padding:50px;'>📦 بوابة الموردين - إدارة المنتجات والأرصدة</h1>"
