from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from . import supplier_bp 
from .auth_logic import verify_supplier_credentials
from .decorators import sovereign_approval_required # 🛡️ حارس بوابة البرزخ

# --- 1. مسار تسجيل الدخول اللامركزي ---
@supplier_bp.route('/login', methods=['GET', 'POST'])
def login():
    # منع التداخل: إذا كان القائد (Admin) يحاول دخول بوابة المورد، يتم تبديل الجلسة
    if current_user.is_authenticated:
        if hasattr(current_user, 'wallet_balance'):
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            logout_user() # تسجيل خروج الإدارة لفتح مجال للمورد

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('يرجى ملء كافة الحقول السيادية للدخول.', 'warning')
            return render_template('supplier_login.html')

        # التحقق من الهوية عبر المحقق الخارجي
        message, category, supplier = verify_supplier_credentials(username, password)
        
        if supplier: 
            login_user(supplier)
            flash(f'تم الولوج بنجاح.. أهلاً بك يا {supplier.name}', 'success')
            
            # 🚀 التعديل: التوجه للداشبورد مباشرة وهو سيتكفل بفحص التعميد
            return redirect(url_for('supplier_panel.dashboard'))
        else:
            flash(message, category)
            
    return render_template('supplier_login.html')

# --- 2. لوحة التحكم (الترسانة الرقمية) ---
@supplier_bp.route('/dashboard')
@login_required
@sovereign_approval_required # 🛡️ هذا الحارس سيقوم بتحويله لـ /waiting-room إذا لم يُعمد
def dashboard():
    from core.models.product import Product
    
    try:
        # 🔒 فحص الرتبة
        if not hasattr(current_user, 'wallet_balance'):
            logout_user()
            flash('عذراً، هذه المنطقة مخصصة لشركاء النجاح فقط.', 'danger')
            return redirect(url_for('supplier_panel.login'))
            
        # 📦 جلب المنتجات
        try:
            my_products = Product.query.filter_by(supplier_id=current_user.id).all()
        except Exception as db_error:
            print(f"⚠️ تنبيه في قاعدة البيانات: {db_error}")
            my_products = []
            
        return render_template('supplier_dashboard.html', products=my_products)
        
    except Exception as e:
        print(f"❌ خطأ داخلي في لوحة المورد: {e}")
        return f"خطأ في النظام (500): {e}", 500

# --- 3. صفحة الانتظار (البرزخ الرقمي) ---
@supplier_bp.route('/waiting-room')
@login_required
def waiting_room():
    """
    هذا المسار هو الذي يتم تحويل المستخدم إليه بواسطة الحارس @sovereign_approval_required
    """
    # إذا تم تعميده وهو هنا، ارسله للداشبورد فوراً
    if hasattr(current_user, 'is_approved') and current_user.is_approved:
        return redirect(url_for('supplier_panel.dashboard'))
    
    # اظهر صفحة الانتظار (تأكد أنها لا ترث من base.html لكي لا يظهر السايدبار)
    return render_template('waiting_approval.html')

# --- 4. خروج المورد وتأمين الترسانة ---
@supplier_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('تم تأمين الجلسة وتشفير الخروج بنجاح.', 'info')
    return redirect(url_for('supplier_panel.login'))
