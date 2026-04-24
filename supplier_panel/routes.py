from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models import Supplier, Product
from . import supplier_bp # استيراد البلوبرنت من ملف __init__.py الخاص بالمجلد

# --- مسار تسجيل الدخول للمورد ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('supplier_panel.dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        supplier = Supplier.query.filter_by(email=email).first()
        
        # ملاحظة: يفضل استخدام check_password_hash للأمان
        if supplier and supplier.password == password:
            login_user(supplier)
            flash(f'مرحباً بك يا {supplier.name} في بوابة شركاء النجاح', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة، يرجى التحقق من البريد وكلمة المرور', 'danger')
            
    return render_template('login.html')

# --- لوحة تحكم المورد ---
@supplier_bp.route('/')
@supplier_bp.route('/dashboard')
@login_required
def dashboard():
    # التحقق من أن المستخدم المشرع هو مورد وليس أدمن (أمان إضافي)
    if not isinstance(current_user, Supplier):
        logout_user()
        return redirect(url_for('supplier_panel.login'))
        
    # جلب منتجات المورد الحالي فقط
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('dashboard.html', products=my_products)

# --- نافذة رفع منتج جديد (سعر التكلفة) ---
@supplier_bp.route('/add_product', methods=['GET', 'POST'])
@login_required
def add_product():
    if request.method == 'POST':
        name = request.form.get('name')
        description = request.form.get('description')
        cost_price = request.form.get('cost_price') # سعر التكلفة من المورد
        image_url = request.form.get('image_url')
        
        new_product = Product(
            name=name,
            description=description,
            original_price=float(cost_price), # تخزين التكلفة
            sale_price=0.0, # يتركه للمورد صفراً، وتحدده الإدارة لاحقاً
            image_url=image_url,
            supplier_id=current_user.id, # ربط المنتج بآيدي المورد الحالي
            status='pending', # المنتج يظل معلقاً حتى تراجعه الإدارة
            is_synced=False   # لا يظهر في قمرة حتى توافق أنت
        )
        
        try:
            db.session.add(new_product)
            db.session.commit()
            flash('✅ تم إرسال المنتج لغرفة العمليات المركزية للمراجعة', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f'⚠️ فشل في إ
