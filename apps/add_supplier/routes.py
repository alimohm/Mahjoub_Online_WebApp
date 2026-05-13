from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from models.supplier_db import db, Supplier  
from datetime import datetime

# تم تثبيت الاسم 'admin_suppliers' ليتوافق مع ملف run.py والهيكل الأساسي
admin_suppliers = Blueprint('admin_suppliers', __name__, template_folder='templates')

@admin_suppliers.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        # استلام البيانات من النموذج (Form)
        supplier_name = request.form.get('supplier_name')
        region = request.form.get('region')  # المناطق المستهدفة: عدن، الخوخة، المخاء
        contact_number = request.form.get('contact_number')
        category = request.form.get('category')

        # التحقق من البيانات الأساسية قبل الحفظ
        if not supplier_name or not region:
            flash('يرجى إدخال اسم المورد والمنطقة لتتم عملية التسجيل.', 'warning')
            return redirect(url_for('admin_suppliers.add_supplier'))

        try:
            # إنشاء سجل المورد الجديد في قاعدة بيانات محجوب أونلاين
            new_supplier = Supplier(
                name=supplier_name,
                region=region,
                contact=contact_number,
                category=category,
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_supplier)
            db.session.commit()
            
            # رسالة نجاح مخصصة تظهر في لوحة التحكم
            flash(f'تم تعميد المورد "{supplier_name}" بنجاح في قطاع {region}.', 'success')
        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ تقني أثناء التسجيل: {str(e)}', 'danger')

        return redirect(url_for('admin_suppliers.add_supplier'))

    # عرض واجهة إضافة المورد (GET request)
    return render_template('add_supplier.html')

@admin_suppliers.route('/api/suppliers-stats')
def suppliers_stats():
    """واجهة برمجية لجلب إحصائيات الموردين لمركز المراقبة والتحكم"""
    try:
        count = Supplier.query.count()
        return jsonify({
            "status": "success",
            "total_suppliers": count,
            "timestamp": datetime.utcnow().isoformat()
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
