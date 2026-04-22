from flask import Blueprint, render_template

admin_bp = Blueprint('admin', __name__, 
                     template_folder='templates', # يشير إلى admin_panel/templates
                     static_folder='static')

@admin_bp.route('/admin/login')
def login():
    # هنا Flask سيبحث داخل admin_panel/templates/admin/login.html
    return render_template('admin/login.html')

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard.html')

@admin_bp.route('/admin/wallets')
def wallets():
    return render_template('admin/wallets.html')

@admin_bp.route('/admin/product-review')
def product_review():
    return render_template('admin/product_review.html')

@admin_bp.route('/admin/order-routing')
def order_routing():
    return render_template('admin/order_routing.html')
