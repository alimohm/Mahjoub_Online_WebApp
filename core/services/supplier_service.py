# admin_panel/supplier_service_routes.py
from flask import render_template, request, jsonify
from flask_login import login_required
from admin_panel import admin_bp
from core.services.supplier_service import update_supplier_profile  # استدعاء المحرك السيادي
from core.models.supplier import Supplier

@admin_bp.route('/suppliers/profile/<int:supplier_id>', methods=['GET', 'POST'])
@login_required
def supplier_profile(supplier_id):
    """
    مسار إدارة بروفايل المورد:
    - GET: جلب البيانات من القاعدة وعرضها في نافذة البروفايل.
    - POST: استقبال بيانات التعديل وتمريرها للمحرك للتعميد والحفظ.
    """
    
    # 1. بروتوكول التحديث (POST)
    if request.method == 'POST':
        try:
            # استخراج البيانات من الفورم القادم عبر AJAX
            data = request.form.to_dict()
            
            # استدعاء المحرك لتنفيذ التعديل في قاعدة البيانات
            # المحرك يحتوي على db.session.commit() لضمان الحفظ
            success, message = update_supplier_profile(supplier_id, data)
            
            if success:
                return jsonify({
                    "status": "success", 
                    "message": "تم تعميد التعديلات بنجاح في السجلات المركزية."
                })
            else:
                return jsonify({
                    "status": "error", 
                    "message": f"فشل التعميد: {message}"
                }), 400
                
        except Exception as e:
            return jsonify({
                "status": "error", 
                "message": f"خطأ تقني في بوابة الخدمات: {str(e)}"
            }), 500

    # 2. بروتوكول العرض (GET)
    # البحث عن الكيان في القاعدة أو إظهار 404 في حال عدم وجوده
    supplier = Supplier.query.get_or_404(supplier_id)
    
    return render_template(
        'suppliers/supplier_profile.html', 
        supplier=supplier
    )
