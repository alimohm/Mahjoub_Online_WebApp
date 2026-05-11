# admin_panel/supplier_service_routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from admin_panel import admin_bp
from core.services.supplier_service import update_supplier_profile
from core.models.supplier import Supplier

@admin_bp.route('/suppliers/profile/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_profile(supplier_id):
    """
    مسار إدارة بروفايل المورد:
    - GET: عرض بيانات المورد الحالية في الواجهة.
    - POST: استقبال طلبات التحديث وتعميدها عبر المحرك المستقل.
    """
    
    # 1. التعامل مع طلبات التعديل (POST) القادمة من AJAX
    if request.method == 'POST':
        try:
            # استخراج البيانات من الفورم
            data = request.form.to_dict()
            
            # استدعاء المحرك المستقل للتنفيذ في قاعدة البيانات
            # نمرر المعرف والبيانات للمحرك لضمان الحوكمة
            success, message = update_supplier_profile(supplier_id, data)
            
            if success:
                return jsonify({
                    "status": "success", 
                    "message": "تم تعميد التحديثات بنجاح في السجلات السيادية"
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"فشل التعميد: {message}"
                }), 400
                
        except Exception as e:
            return jsonify({
                "status": "error", 
                "message": f"خطأ في الاتصال بالمحرك: {str(e)}"
            }), 500

    # 2. التعامل مع طلبات العرض (GET)
    # جلب بيانات المورد أو إظهار صفحة 404 إذا لم يوجد
    supplier = Supplier.query.get_or_404(supplier_id)
    
    return render_template(
        'suppliers/supplier_profile.html', 
        supplier=supplier
    )
