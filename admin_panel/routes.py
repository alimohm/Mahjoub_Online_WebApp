from flask import render_template, request, redirect, url_for, flash, session
from flask_login import login_required, logout_user
from core import db 

# استيراد النماذج (Models) بمساراتها الصحيحة من قلب النظام
try:
    from core.models import Vendor, User
    from core.models.vendor import WithdrawRequest
except ImportError:
    WithdrawRequest = None
    Vendor = None
    User = None

from . import admin_bp
from .auth import handle_admin_login  # استيراد محرك التحقق المركزي

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """بوابة الدخول السيادية لمركز القيادة - محجوب أونلاين"""
    # تفويض المهمة لمحرك التحقق في auth.py لمنع تضارب المنطق
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    """إغلاق جلسة الوصول وتأمين النظام بالكامل"""
    logout_user() # إنهاء جلسة القائد بشكل آمن
    session.clear()
    flash("تم تسجيل الخروج وتأمين مركز القيادة بنجاح.", "info")
    return redirect(url_for('admin.login'))

@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    """مركز المراقبة والإحصائيات الرئيسي لإدارة العمليات في اليمن"""
    # نظام flask_login يتكفل بالتحقق من الهوية عبر @login_required
    return render_template('dashboard.html')

@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    """عرض كافة طلبات تصفية الأرصدة المعلقة للموردين"""
    if WithdrawRequest is None:
        flash("تنبيه: نظام طلبات السحب غير مفعل في الترسانة حالياً.", "warning")
        return render_template('withdraw_requests.html', requests=[])
    
    try:
        # جلب الطلبات المعلقة مرتبة من الأحدث إلى الأقدم
        pending_requests = WithdrawRequest.query.filter_by(status='pending').order_by(WithdrawRequest.created_at.desc()).all()
        return render_template('withdraw_requests.html', requests=pending_requests)
    except Exception as e:
        flash(f"حدث خلل في جلب البيانات من الترسانة: {str(e)}", "danger")
        return render_template('withdraw_requests.html', requests=[])

@admin_bp.route('/finalize-withdrawal', methods=['POST'])
@login_required
def finalize_withdrawal():
    """تعميد الحوالات المالية وأرشفتها في سجلات المنصة"""
    request_id = request.form.get('request_id')
    bank_name = request.form.get('bank_name')
    reference_number = request.form.get('reference_number')

    withdrawal_entry = WithdrawRequest.query.get(request_id)
    if withdrawal_entry:
        try:
            withdrawal_entry.status = 'completed'
            withdrawal_entry.bank_used = bank_name
            withdrawal_entry.reference_id = reference_number
            db.session.commit()
            flash(f"تم تعميد الحوالة برقم مرجعي ({reference_number}) بنجاح.", "success")
        except Exception as e:
            db.session.rollback()
            flash(f"فشل نظام الأرشفة الرقمي: {str(e)}", "danger")
    
    return redirect(url_for('admin.withdraw_requests'))

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """إضافة مورد جديد لشبكة محجوب أونلاين"""
    if request.method == 'POST':
        name = request.form.get('name')
        city = request.form.get('city')
        try:
            # إنشاء سجل المورد الجديد في قاعدة البيانات
            new_vendor = Vendor(name=name, city=city)
            db.session.add(new_vendor)
            db.session.commit()
            flash(f"تمت إضافة المورد ({name}) إلى شبكة التوزيع بنجاح.", "success")
            return redirect(url_for('admin.admin_dashboard'))
        except Exception as e:
            db.session.rollback()
            flash(f"خطأ في حفظ بيانات المورد: {str(e)}", "danger")

    return render_template('add_supplier.html')
