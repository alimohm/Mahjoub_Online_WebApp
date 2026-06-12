from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps import db
from apps.models.bridge_db import Product, ProductVariant # استيراد الموديلات من مجلد المودلز الحالي

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/bridge/dashboard', methods=['GET'])
def dashboard():
    # جلب المنتجات من قاعدة البيانات المحلية مباشرة (Pagination)
    page = request.args.get('page', 1, type=int)
    per_page = 16
    
    # استعلام لجلب المنتجات مع المتغيرات الخاصة بها
    pagination = Product.query.order_by(Product.created_at.desc()).paginate(page=page, per_page=per_page)
    products = pagination.items
    
    return render_template('admin/bridge_dashboard.html', products=products, page=page)

@bridge_bp.route('/bridge/add-product', methods=['GET', 'POST'])
def add_product_page():
    if request.method == 'POST':
        # منطق إضافة منتج جديد يدوياً إلى قاعدة البيانات
        new_product = Product(
            title=request.form.get('title'),
            description=request.form.get('description'),
            price=float(request.form.get('price', 0)),
            quantity=int(request.form.get('quantity', 0)),
            supplier_id=request.form.get('supplier_id')
        )
        db.session.add(new_product)
        db.session.commit()
        flash('تم إضافة المنتج محلياً بنجاح', 'success')
        return redirect(url_for('mahjoub_bridge.dashboard'))
    
    return render_template('admin/add_product.html')

@bridge_bp.route('/bridge/sync-now', methods=['POST'])
def sync_now():
    """
    هذا المسار مخصص لأي عمليات تحديث محلية تحتاجها، 
    بما أننا لا نزامن مع قمرة، يمكنك هنا إضافة منطق تحديث الأسعار 
    أو الكميات بناءً على جداول الموردين المخزنة لديك.
    """
    try:
        # هنا تضع منطق المزامنة المحلية الخاص بك (مثلاً تحديث المخزون)
        return jsonify({"status": "success", "message": "تم تحديث البيانات من قاعدة البيانات المحلية"})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
