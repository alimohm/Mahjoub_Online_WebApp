from flask import render_template, request, redirect, url_for, flash
# استيراد db من النواة
from core import db 

# تصحيح الخطأ الجذري: الاستيراد من المسار المعتمد في مشروعك
try:
    # بما أن core/models/__init__.py يستورد Vendor، فنحن نستورده من هناك
    from core.models import Vendor
    # إذا كان WithdrawRequest موجوداً داخل ملف vendor.py استورده هكذا:
    from core.models.vendor import WithdrawRequest
except ImportError:
    # محاولة استيراد في حال كان الموديل معرفاً في مكان آخر داخل النماذج
    from core.models.user import User
    # ملاحظة: تأكد أن كلاس WithdrawRequest موجود فعلياً داخل ملف vendor.py
    flash("تنبيه: تأكد من وجود كلاس WithdrawRequest داخل ملف vendor.py", "warning")

# استيراد البلوبرنت
from . import admin_bp

@admin_bp.route('/withdraw-requests')
def withdraw_requests():
    """عرض كافة طلبات تصفية الأرصدة المعلقة"""
    try:
        # جلب البيانات (تأكد من أن اسم الموديل WithdrawRequest)
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """تعميد الحوالة وأرشفة البيانات سيادياً"""
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("يرجى إدخال رقم الحوالة ياقائد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if withdrawal_entry:
        try:
            withdrawal_entry.status = 'completed'
            withdrawal_entry.bank_used = bank_name
            withdrawal_entry.reference_id = reference_number
            db.session.commit()
            flash(f"تم اعتماد الحوالة رقم {reference_number} بنجاح.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"خطأ في الحفظ: {str(e)}", "danger")
    
    return redirect(url_for('admin.withdraw_requests'))
