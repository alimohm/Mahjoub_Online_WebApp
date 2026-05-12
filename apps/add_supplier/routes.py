from flask import Blueprint, render_template, request, jsonify, redirect, url_for, session, flash
from models.supplier_db import db, Supplier

# تعريف الـ Blueprint مع تحديد مجلد القوالب بدقة
add_supplier_bp = Blueprint(
    'add_supplier', 
    __name__, 
    template_folder='templates' # يشير إلى مجلد templates داخل add_supplier
)

# المسار السيادي لإضافة الموردين (يدعم العرض GET والحفظ POST)
@add_supplier_bp.route('/supplier/add', methods=['GET', 'POST'])
def save_supplier():
    # 🛡️ التحقق من صلاحية المؤسس قبل عرض الصفحة أو معالجة البيانات
    if not session.get('is_authenticated'):
        return redirect(url_for('auth.login'))

    # --- أولاً: حالة العرض (GET) ---
    if request.method == 'GET':
        try:
            # حساب المعرف القادم لإظهاره في الواجهة
            last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
            next_id_count = (last_supplier.id + 1) if last_supplier else 1
            
            # استدعاء قالب إضافة المورد الموجود داخل admin
            # المسار الفعلي: apps/add_supplier/templates/admin/add_supplier.html
            return render_template('admin/add_supplier.html', next_id=next_id_count)
        except Exception as e:
            # في حال وجود خطأ في قاعدة البيانات عند العرض
            return f"Error loading supplier page: {str(e)}", 500

    # --- ثانياً: حالة الحفظ (POST) ---
    if request.method == 'POST':
        # استقبال البيانات سواء كانت JSON (AJAX) أو Form Data عادية
        data = request.get_json() if request.is_json else request.form
        
        try:
            # 1. إنشاء كائن المورد الجديد وربطه بالبيانات القادمة
            new_supplier = Supplier(
                username=data.get('username'),
                password=data.get('password'),
                trade_name=data.get('trade_name'),
                owner_name=data.get('owner_name'),
                phone=data.get('phone'),
                activity_type=data.get('activity_type'),
                province=data.get('province'),
                district=data.get('district'),
                address_detail=data.get('address_detail'),
                bank_name=data.get('bank_name'),
                bank_acc=data.get('bank_acc')
            )

            # 2. توليد المعرف السيادي (Sovereign ID) تلقائياً بناءً على العدد الحالي
            count = Supplier.query.count() + 1
            new_supplier.sovereign_id = f"SUP-MHA_963{count}"

            # 3. التنفيذ الفوري والحفظ في قاعدة بيانات Postgres
            db.session.add(new_supplier)
            db.session.commit()

            # الاستجابة حسب نوع الطلب
            if request.is_json:
                return jsonify({
                    'status': 'success', 
                    'message': f'تم تعميد المورد بنجاح بالرقم: {new_supplier.sovereign_id}'
                })
            
            flash(f'تم حفظ المورد {new_supplier.trade_name} بنجاح.', 'success')
            return redirect(url_for('admin.dashboard'))

        except Exception as e:
            # التراجع عن العملية في حال حدوث خطأ لمنع تضرر قاعدة البيانات
            db.session.rollback()
            error_msg = f"فشلت عملية الأرشفة: {str(e)}"
            if request.is_json:
                return jsonify({'status': 'error', 'message': error_msg}), 500
            
            flash(error_msg, 'danger')
            return redirect(url_for('add_supplier.save_supplier'))
