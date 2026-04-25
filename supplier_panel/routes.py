from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from core import db
from core.models import Supplier, Product
from . import supplier_bp 

# --- 1. مسار تسجيل الدخول مع التحقق الصارم ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم مسجلاً بالفعل، لا داعي لإظهار صفحة الدخول
    if current_user.is_authenticated:
        if isinstance(current_user, Supplier):
            return redirect(url_for('supplier_panel.dashboard'))

    if request.method == 'POST':
        # استقبال البيانات من الواجهة الملكية
        username = request.form.get('username')
        password = request.form.get('password')

        # 🛡️ التحقق الأول: هل الحقول فارغة؟
        if not username or not password:
            flash('يرجى إدخال اسم المورد وكلمة المرور معاً.', 'warning')
            return render_template('supplier_login.html')

        # 🔍 التحقق الثاني: البحث عن المورد في قاعدة البيانات
        # نستخدم .first() لضمان جلب مورد واحد فقط بدقة
        supplier = Supplier.query.filter_by(name=username).first()

        # 🔑 التحقق الثالث: مطابقة كلمة المرور
        if supplier and supplier.password == password:
            # تم التحقق بنجاح -> تسجيل الدخول
            login_user(supplier)
            flash(f'مرحباً بك يا {supplier.name}.. تم التحقق من الهوية بنجاح.', 'success')
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            # فشل التحقق -> رسالة أمان غامضة (لأغراض أمنية)
            flash('عذراً، بيانات الدخول غير صحيحة. يرجى التثبت والمحاولة مجدداً.', 'danger')
            
    return render_template('supplier_login.html')

# --- 2. حماية لوحة التحكم ---
@supplier_bp.route('/dashboard')
@login_required # لا يمكن الدخول هنا إلا بحساب نشط
def dashboard():
    # 🚫 منع "الأدمن" من دخول لوحة "المورد" والعكس
    if not isinstance(current_user, Supplier):
        logout_user() # طرد أي مستخدم ليس مورداً
        flash('هذا المسار مخصص لشركاء النجاح فقط.', 'danger')
        return redirect(url_for('supplier_panel.login'))
        
    my_products = Product.query.filter_by(supplier_id=current_user.id).all()
    return render_template('supplier_dashboard.html', products=my_products)
