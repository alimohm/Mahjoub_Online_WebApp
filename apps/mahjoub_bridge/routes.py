# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from apps import db
from apps.models.bridge_db import Product, ProductVariant, encrypt, decrypt
from apps.utils.bridge_engine import QumraBridgeEngine

bridge_bp = Blueprint('mahjoub_bridge', __name__, template_folder='templates')

@bridge_bp.route('/dashboard', methods=['GET'])
def dashboard():
    """عرض لوحة التحكم مع تأمين فك التشفير"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = 16
        pagination = Product.query.order_by(Product.id.desc()).paginate(page=page, per_page=per_page, error_out=False)
        products = pagination.items
        
        def safe_decrypt(value):
            if not value: return "0.00"
            try:
                return decrypt(value)
            except:
                return "0.00"

        return render_template('admin/bridge_dashboard.html', 
                               products=products, 
                               pagination=pagination, 
                               page=page, 
                               decrypt=safe_decrypt)
                               
    except Exception as e:
        print(f"Error in bridge dashboard: {str(e)}")
        flash(f"حدث خطأ: {str(e)}", "danger")
        return redirect(url_for('admin_dashboard.dashboard'))

@bridge_bp.route('/add-product', methods=['GET', 'POST'])
def add_product_page():
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            if not title:
                flash('عنوان المنتج مطلوب!', 'warning')
                return redirect(url_for('mahjoub_bridge.add_product_page'))
                
            raw_price = request.form.get('price', '0')
            encrypted_price = encrypt(str(raw_price))
            qty = int(request.form.get('quantity', 0))
            
            new_product = Product(
                title=title,
                description=request.form.get('description', ''),
                price=encrypted_price,
                quantity=qty,
                supplier_id=request.form.get('supplier_id')
            )
            db.session.add(new_product)
            db.session.commit()
            flash('تم إضافة المنتج بنجاح', 'success')
            return redirect(url_for('mahjoub_bridge.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'خطأ أثناء الحفظ: {str(e)}', 'danger')
    return render_template('admin/add_product.html')

@bridge_bp.route('/sync-now', methods=['POST'])
def sync_now():
    """المزامنة اللحظية مع تنظيف صارم للبيانات"""
    try:
        engine = QumraBridgeEngine()
        raw_products = engine.fetch_latest_products(limit=20)
        
        if not raw_products:
            return jsonify({"status": "warning", "message": "لا توجد منتجات جديدة"})

        count = 0
        for item in raw_products:
            # حماية قصوى: التأكد أن العنوان ليس None
            title_raw = item.get('title')
            if title_raw is None: continue
            title = str(title_raw).strip()
            if not title: continue 
            
            if not Product.query.filter_by(title=title).first():
                # تنظيف السعر
                pricing = item.get('pricing') or {}
                raw_price = pricing.get('price') or "0"
                
                # تنظيف الكمية
                raw_qty = item.get('quantity') or 0
                
                # التخزين
                new_product = Product(
                    title=title,
                    description="تمت المزامنة",
                    price=encrypt(str(raw_price)),
                    quantity=int(raw_qty),
                    supplier_id="QUMRA_SYNC"
                )
                db.session.add(new_product)
                count += 1
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تمت المزامنة بنجاح وجلب {count} منتج"})
        
    except Exception as e:
        db.session.rollback()
        print(f"CRITICAL SYNC ERROR: {str(e)}")
        return jsonify({"status": "error", "message": "حدث خطأ في المزامنة"}), 500
