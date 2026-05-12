from flask import Blueprint, render_template

# اسم البلوبرنت 'admin' هو المفتاح لربط url_for('admin.xxx')
admin_bp = Blueprint('admin', __name__, template_folder='templates')

@admin_bp.route('/admin/dashboard')
def dashboard():
    return render_template('admin/dashboard_content.html')

@admin_bp.route('/admin/suppliers/add')
def add_supplier():
    # مؤقتاً نعيد صفحة بسيطة تتبع الهيكل الملكي
    return render_template('admin/dashboard_content.html', title="تعميد كيان جديد")

@admin_bp.route('/admin/suppliers/manage')
def manage_suppliers():
    return render_template('admin/dashboard_content.html', title="الموردون المعتمدون")

@admin_bp.route('/admin/staff/manage')
def manage_staff():
    # هذا الرابط مطلوب في قسم 'حوكمة الصلاحيات' بقالبك
    return "لوحة إدارة طاقم الإدارة العليا - قيد التجهيز"

@admin_bp.route('/admin/logout')
def logout():
    return "تم إنهاء الجلسة السيادية بنجاح."
