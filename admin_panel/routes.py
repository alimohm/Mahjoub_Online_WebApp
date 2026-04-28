from flask import render_template, redirect, url_for, flash, request, Blueprint
from flask_login import login_required, current_user, login_user, logout_user
from core.models.user import User  # استيراد الموديل من قلب النظام

# 1. تعريف البلوبرينت (هذا هو السطر الذي كان ينقصك ويسبب الخطأ الفادح)
admin_bp = Blueprint(
    'admin_panel', 
    __name__, 
    template_folder='templates'
)

# ==========================================
# 1. بوابة الدخول (login.html)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def admin_login():
    if current_user.is_authenticated and current_user.role == 'admin':
        return redirect(url_for('admin_panel.admin_dashboard'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email, role='admin').first()
        
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('admin_panel.admin_dashboard'))
        else:
            flash('بيانات الدخول غير صحيحة يا قائد.', 'danger')
            
    return render_template('admin_panel/login.html')

# ==========================================
# 2. لوحة التحكم المركزية (dashboard.html)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    return render_template('admin_panel/dashboard.html')

# ==========================================
# 3. إدارة الموردين (admin_suppliers_management.html)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def admin_suppliers_management():
    # هنا سيتم لاحقاً جلب قائمة الموردين من قاعدة البيانات
    return render_template('admin_panel/admin_suppliers_management.html')

# ==========================================
# 4. المركز المالي (wallets.html)
# ==========================================
@admin_bp.route('/wallets')
@login_required
def wallets():
    return render_template('admin_panel/wallets.html')

# ==========================================
# 5. مراجعة المنتجات (product_review.html)
# ==========================================
@admin_bp.route('/reviews')
@login_required
def product_review():
    return render_template('admin_panel/product_review.html')

# ==========================================
# 6. تفاصيل المنتج (product_detail.html)
# ==========================================
@admin_bp.route('/product/<int:id>')
@login_required
def product_detail(id):
    return render_template('admin_panel/product_detail.html')

# ==========================================
# 7. تسجيل الخروج
# ==========================================
@admin_bp.route('/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_panel.admin_login'))
