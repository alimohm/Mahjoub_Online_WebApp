# admin_panel/supplier_service_routes.py
from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required
from admin_panel import admin_bp
from core.models.supplier import Supplier

@admin_bp.route('/suppliers/profile/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_profile(supplier_id):
    """
    مسار إدارة بروفايل المورد السيادي:
    - GET: عرض بيانات المورد وطاقم العمل.
    - POST (AJAX): تحديث الحقول بشكل فردي (الحفظ التلقائي).
    - POST (Form): إضافة موظفين جدد لطاقم العمل.
    """
    
    # 1. بروتوكول التحديث القادم من AJAX (الحفظ التلقائي)
    if request.method == 'POST' and request.is_json:
        from core.services.supplier_service import update_supplier_field
        
        try:
            data = request.get_json()
            field = data.get('field')
            value = data.get('value')
            
            # تنفيذ عملية التعميد للحقل المحدد فقط لسرعة الأداء
            success, message = update_supplier_field(supplier_id, field, value)
            
            if success:
                return jsonify({
                    "status": "success", 
                    "message": "تم تعميد التحديث بنجاح."
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"فشل التعميد: {message}"
                }), 400
                
        except Exception as e:
            return jsonify({
                "status": "error", 
                "message": f"خطأ في المحرك: {str(e)}"
            }), 500

    # 2. بروتوكول إضافة موظف جديد (من المودال)
    if request.method == 'POST' and 'new_username' in request.form:
        from core.services.supplier_service import add_staff_to_supplier
        
        staff_data = {
            'username': request.form.get('new_username'),
            'name': request.form.get('full_name'),
            'password': request.form.get('new_password')
        }
        
        success, message = add_staff_to_supplier(supplier_id, staff_data)
        
        if success:
            flash(f"✅ {message}", "success")
        else:
            flash(f"⚠️ {message}", "danger")
            
        return redirect(url_for('admin.supplier_profile', supplier_id=supplier_id))

    # 3. بروتوكول العرض (GET)
    supplier = Supplier.query.get_or_404(supplier_id)
    
    return render_template(
        'suppliers/supplier_profile.html', 
        supplier=supplier
    )
