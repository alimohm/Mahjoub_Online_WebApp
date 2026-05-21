# coding: utf-8
# 🏢 محرك تعميد الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from apps import db
from apps.models.supplier_db import Supplier

# تعريف الـ Blueprint الخاص بالموردين
admin_suppliers_bp = Blueprint('add_supplier', __name__)

@admin_suppliers_bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier_submit():
    """
    دالة معالجة تعميد (إضافة) مورد جديد
    """
    if request.method == 'POST':
        # هنا يتم استلام البيانات من النموذج وحفظها في قاعدة البيانات
        # تأكد من تطابق أسماء الحقول مع الفورم في صفحة الـ HTML
        try:
            name = request.form.get('name')
            wallet_code = request.form.get('wallet_code')
            
            # مثال لإنشاء المورد (يجب تعديل الحقول حسب قاعدة بياناتك)
            new_supplier = Supplier(name=name, wallet_code=wallet_code)
            db.session.add(new_supplier)
            db.session.commit()
            
            flash('تم تعميد المورد بنجاح', 'success')
            return redirect(url_for('admin_dashboard.list_suppliers'))
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء التعميد: {str(e)}', 'danger')

    return render_template('suppliers/add_supplier.html')

# يمكنك إضافة مسارات أخرى هنا إذا لزم الأمر
