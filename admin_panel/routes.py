from flask import render_template, request, redirect, url_for, flash
# استيراد db من النواة لضمان تزامن البيانات مع القاعدة الجديدة
from core import db 

# استيراد النماذج (Models) بمساراتها الصحيحة داخل مجلد core
try:
    from core.models import Vendor, User
    # تأكد أن WithdrawRequest موجود داخل ملف vendor.py أو مستورد في __init__.py الخاص بالنماذج
    from core.models.vendor import WithdrawRequest
except ImportError:
    # تعريف بديل لمنع انهيار النظام في حال لم يتم رفع الموديلات بعد
    WithdrawRequest = None
    Vendor = None

# استيراد البلوبرنت الخاص بالإدارة المعرف في admin_panel/__init__.py
from . import admin_bp

@admin_bp.route('/dashboard')
def admin_dashboard():
    """
    مركز المراقبة والإحصائيات الرئيسي (المرحلة الثانية)
    """
    return render_template('dashboard.html')

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """
    عرض كافة طلبات تصفية الأرصدة المعلقة للموردين
    """
    if WithdrawRequest is None:
        flash("تنبيه: نظام طلبات السحب غير مفعل في الموديلات حالياً.", "warning")
        return render_template('withdraw_requests.html', requests=[])
    
    try:
        # جلب الطلبات المعلقة وترتيبها من الأحدث لضمان سرعة التعميد
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب بيانات السحب: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """
    دالة التعميد المالي لتوثيق الحوالات وأرشفتها في سجلات محجوب أونلاين
    """
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("يجب إدخال رقم الحوالة المرجعي لإتمام التعميد ياقائد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على السجل المطلوب.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات الأرشفة السيادية
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        db.session.commit()
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"فشل نظام الأرشفة: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    """
    إضافة مورد جديد إلى الترسانة الرقمية بناءً على مبدأ الثقة
    """
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        
        if Vendor is None:
            flash("خطأ: موديل الموردين غير معرف.", "danger")
            return redirect(url_for('admin.add_supplier'))

        try:
            new_vendor = Vendor(name=name, city=city)
            db.session.add(new_vendor)
            db.session.commit()
            flash(f"تم إضافة المورد ({name}) بنجاح إلى شبكة محجوب أونلاين.", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"حدث خطأ أثناء حفظ المورد: {str(e)}", "danger")

    return render_template('add_supplier.html')
