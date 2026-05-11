# admin_panel/supplier_service_routes.py
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from admin_panel import admin_bp
from core import db
from core.models.supplier import Supplier, SupplierStaff

@admin_bp.route('/suppliers/profile/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_profile(supplier_id):
    """
    مسار إدارة بروفايل المورد السيادي:
    - GET: عرض بيانات المورد وطاقم العمل.
    - POST (AJAX): تحديث الحقول بشكل فردي (الحفظ التلقائي).
    - POST (Form): إضافة موظفين جدد لطاقم العمل.
    """
    supplier = Supplier.query.get_or_404(supplier_id)

    # 1. بروتوكول التحديث القادم من AJAX (الحفظ التلقائي للحقول)
    if request.method == 'POST' and request.is_json:
        try:
            data = request.get_json()
            field = data.get('field')
            value = data.get('value')
            
            # منع تعديل كلمة المرور عبر AJAX (يجب استخدام مسار الـ Reset المخصص)
            if field == 'password':
                return jsonify({
                    "status": "error", 
                    "message": "تعديل كلمة المرور محظور عبر هذا البروتوكول."
                }), 403

            # التأكد من وجود الحقل في كائن المورد وتحديثه
            if hasattr(supplier, field):
                setattr(supplier, field, value)
                db.session.commit()
                return jsonify({
                    "status": "success", 
                    "message": f"تم تعميد تحديث {field} بنجاح."
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"الحقل '{field}' غير معرّف في النظام."
                }), 400
                
        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error", 
                "message": f"عطل في محرك المزامنة: {str(e)}"
            }), 500

    # 2. بروتوكول إضافة موظف جديد (من نافذة المودال)
    if request.method == 'POST' and 'new_username' in request.form:
        try:
            username = request.form.get('new_username')
            name = request.form.get('full_name')
            password = request.form.get('new_password')
            
            # التحقق من توفر اسم المستخدم
            existing_user = SupplierStaff.query.filter_by(username=username).first()
            if existing_user:
                flash(f"⚠️ اسم المستخدم {username} محجوز مسبقاً.", "danger")
                return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

            new_staff = SupplierStaff(
                supplier_id=supplier_id,
                username=username,
                name=name
            )
            new_staff.set_password(password)
            
            db.session.add(new_staff)
            db.session.commit()
            flash(f"✅ تم تعميد الموظف {name} وإلحاقه بالكيان بنجاح.", "success")
            
        except Exception as e:
            db.session.rollback()
            flash(f"⚠️ فشلت عملية الإلحاق: {str(e)}", "danger")
            
        return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

    # 3. بروتوكول العرض السيادي (GET)
    return render_template(
        'suppliers/supplier_profile.html', 
        supplier=supplier
    )

@admin_bp.route('/suppliers/reset-password/<int:supplier_id>', methods=['POST'])
@login_required
def reset_supplier_password(supplier_id):
    """
    بروتوكول إعادة تعيين كلمة المرور السيادية للمورد (في حال النسيان)
    """
    supplier = Supplier.query.get_or_404(supplier_id)
    new_password = request.form.get('new_password')

    if not new_password:
        flash("⚠️ لم يتم استقبال كلمة مرور جديدة.", "warning")
        return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

    try:
        # تشفير كلمة المرور الجديدة وحفظها
        supplier.set_password(new_password)
        db.session.commit()
        flash(f"✅ تم تصفير كلمة مرور الكيان {supplier.trade_name} بنجاح.", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"⚠️ عطل في بروتوكول التصفير: {str(e)}", "danger")

    return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

"""
--- ملاحظات حوكمة النظام ---
1. تم فصل "تصفير كلمة المرور" في مسار مستقل لضمان تطبيق دوال التشفير (Hashing) بشكل صحيح.
2. النظام الآن يدعم الحفظ التلقائي لاسم المستخدم (Username) مع إمكانية استعادة الوصول عبر Reset Password.
3. جميع العمليات مسجلة في قاعدة بيانات "محجوب أونلاين".
"""
