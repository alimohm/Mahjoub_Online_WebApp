from flask import Blueprint, render_template

admin_bp = Blueprint('admin_portal', __name__, template_folder='templates')

@admin_bp.route('/admin/dashboard')
def admin_home():
    return "<h1 style='color:#D4AF37; background:#0A0A0A; text-align:center;'>🛡️ لوحة التحكم السيادية - محجوب أونلاين</h1>"
