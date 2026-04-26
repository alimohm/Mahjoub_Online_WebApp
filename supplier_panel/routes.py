from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required 
from core import db
from core.models.product import Product
from core.models.supplier import Supplier
# استخدام المحرك الجديد والخفيف
from services.qumra_handler import fetch_qumra_collections

# --- 1. مسار تسجيل الدخول السيادي ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if session.get('user_type') == 'supplier':
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            logout_user()
            session.clear()

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى ملء كافة الحقول السيادية للدخول.', 'warning')
            return render_template('supplier_login.html')

        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            session.permanent = True
            session['user_type'] = 'supplier'
            login_user(supplier)
            flash(f'تم الولوج بنجاح.. أهلاً بك يا {supplier.name}', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required 
def dashboard():
    try:
        if session.get('user_type') != 'supplier':
            session.clear()
            logout_user()
            return redirect(url_for('supplier_panel.login'))
            
        # جلب منتجات المورد الحالي فقط
        my_products = Product.query.filter_by(supplier_id=current_user.id).all()
        return render_template('dashboard.html', products=my_products)
        
    except Exception as e:
        return f"خطأ في النظام السيادي: {str(e)}", 500

# --- 3. إضافة منتج جديد (الربط الخفيف مع قمرة) ---
@supplier_bp.route('/add-product', methods=['GET', 'POST'])
@login_required
@sovereign_approval_required
def add_product():
    # سحب الأقسام "لحظياً" من قمرة دون تخزينها محلياً
    collections = fetch_qumra_collections()

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        collection_id = request.form.get('collection_id')
        cost_price = request.form.get('cost_price')
        currency = request.form.get('currency')
        
        if not name or not cost_price:
            flash('يرجى إدخال اسم المنتج وسعر التكلفة لضمان الحوكمة.', 'danger')
            return redirect(request.url)

        try:
            # إنشاء كائن المنتج في الترسانة المحلية (حالة الانتظار)
            new_product = Product(
                name=name,
                description=description,
                q_collection_id=collection_id,
                cost_price=float(cost_price),
                currency=currency,
                supplier_id=current_user.id,
                status='pending' # يبقى معلقاً حتى تعميده من "برج الرقابة"
            )
            
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم رفع المنتج بنجاح وهو بانتظار المراجعة السيادية في برج الرقابة.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ حدث خطأ أثناء المعالجة: {str(e)}', 'danger')

    return render_template('add_product.html', collections=collections)

# --- 4. صفحة الانتظار (للموردين غير المعتمدين) ---
@supplier_bp.route('/waiting-room')
@login_required
def waiting_room():
    # التحقق من الحالة اللحظية للمورد من قاعدة البيانات
    supplier = Supplier.query.get(current_user.id)
    if supplier and supplier.is_approved:
        return redirect(url_for('supplier_panel.dashboard'))
    
    return render_template('waiting_approval.html')

# --- 5. خروج آمن ---
@supplier_bp.route('/logout')
@login_required
def logout():
    session.pop('user_type', None)
    session.clear()
    logout_user()
    return redirect(url_for('supplier_panel.login'))
