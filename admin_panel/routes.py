from flask import Blueprint, render_template, request, redirect, url_for, flash
# الحل الجذري للمشكلة الموضحة في صورة image_a37ff4.png:
# يجب الاستيراد من المسار الصحيح للمشروع (app هو المجلد الرئيسي)
from app import db 
from app.models import WithdrawRequest, Vendor 

# ملاحظة: في بعض الهيكليات قد تحتاج لتغيير الاستيراد أعلاه إلى:
# from core import db (إذا كان db معرفاً داخل مجلد core كما يظهر في سجلات الخطأ)

# تعريف الـ Blueprint باسم يتوافق مع ما تم تسجيله في __init__.py
admin = Blueprint('admin', __name__)

@admin.route('/withdraw-requests')
def withdraw_requests():
    """
    عرض كافة طلبات تصفية الأرصدة المعلقة للموردين.
    """
    try:
        # جلب الطلبات المعلقة وترتيبها من الأحدث
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خطأ أثناء جلب البيانات: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin.route('/finalize-withdrawal', methods=['POST'])
def finalize_withdrawal():
    """
    دالة التعميد المالي السيادي لأرشفة بيانات التحويل.
    """
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    if not request_id or not reference_number:
        flash("تنبيه: يجب إدخال رقم الحوالة المرجعي لإتمام عملية التعميد ياقائد.", "warning")
        return redirect(url_for('admin.withdraw_requests'))

    # البحث عن طلب السحب باستخدام المعرف الفريد
    withdrawal_entry = WithdrawRequest.query.get(request_id)

    if not withdrawal_entry:
        flash("خطأ: لم يتم العثور على سجل لهذا الطلب في النظام.", "danger")
        return redirect(url_for('admin.withdraw_requests'))

    try:
        # تحديث بيانات السجل المالي للتعميد
        withdrawal_entry.status = 'completed'
        withdrawal_entry.bank_used = bank_name
        withdrawal_entry.reference_id = reference_number
        
        # حفظ التغييرات نهائياً في قاعدة بيانات محجوب أونلاين
        db.session.commit()
        
        flash(f"تم تعميد الحوالة رقم ({reference_number}) بنجاح وأرشفة الطلب.", "success")
        
    except Exception as e:
        db.session.rollback() # التراجع في حالة وجود خطأ تقني
        flash(f"فشل نظام الأرشفة في معالجة الطلب: {str(e)}", "danger")

    return redirect(url_for('admin.withdraw_requests'))
