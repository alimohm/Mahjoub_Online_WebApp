from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models import Supplier, Product
from . import supplier_bp 

# --- 1. مسار تسجيل الدخول ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if isinstance(current_user, Supplier):
            return redirect(url_for('supplier_panel.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # البحث بالاسم العربي كما في الواجهة الملكية
        supplier = Supplier.query.filter_by(name=username).first()
        
        if supplier and supplier.password == password:
            login_user(supplier)
            flash(f'أهلاً بك يا {supplier.name} في منصة محجوب أونلاين', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash('خطأ في اسم المورد أو كلمة المرور، يرجى المحاولة مرة أخرى.', 'danger')
            
    return render_template('supplier_login.html')

# --- 2. لوحة تحكم المورد ---
@supplier_bp.route('/')
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    if not isinstance(current_user, Supplier):
        logout_user()
        flash('عذراً، هذه المنطقة مخصصة للموردين فقط.', 'warning')
        return redirect(url_for('supplier_panel.login'))
        
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('supplier_dashboard.html', products=my_products)

# --- 3. رفع منتج جديد ---
@supplier_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if not isinstance(current_user, Supplier):
        return redirect(url_for('supplier_panel.login'))

    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cost_price = request.form.get('cost_price')
        image_url = request.form.get('image_url')
        
        new_product = Product(
            name=name,
            description=description,
            original_price=float(cost_price) if cost_price else 0.0,
            sale_price=0.0,
            image_url=image_url,
            supplier_id=current_user.id,
            status='pending',
            is_synced=False
        )
        
        try:
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم إرسال المنتج للمراجعة السيادية بنجاح.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ فشل الحفظ: {str(e)}', 'danger')

    return render_template('supplier_add_product.html')

# --- 4. تسجيل الخروج ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تسجيل الخروج من بوابة الشركاء بنجاح.', 'info')
    return redirect(url_for('supplier_panel.login'))
