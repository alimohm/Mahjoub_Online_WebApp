from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from models.supplier_db import db, Supplier
import os

# تعديل تعريف الـ Blueprint لضمان الاستقرار
add_supplier_bp = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates',
    static_folder='static' # إضافة مجلد الاستاتيك إذا لزم الأمر
)

@add_supplier_bp.route('/supplier/add', methods=['GET', 'POST'])
def add_supplier():
    # التحقق من الجلسة
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))

    if request.method == 'GET':
        try:
            # استخدام count() بدلاً من جلب كافة السجلات لتحسين الأداء وتجنب الـ Timeout
            next_id_count = Supplier.query.count() + 1
            return render_template('admin/add_supplier.html', next_id=next_id_count)
        except Exception as e:
            # طباعة الخطأ في الـ Logs لمساعدتنا في تشخيص الصورة القادمة
            print(f"CRITICAL ERROR in GET /supplier/add: {str(e)}")
            return f"Error loading supplier page: {str(e)}", 500
