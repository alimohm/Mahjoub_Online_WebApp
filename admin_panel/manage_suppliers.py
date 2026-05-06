from flask import render_template, request, jsonify, redirect, url_for, flash
from flask_login import login_required, current_user
from core.extensions import db
from core.models.supplier import Supplier
# استيراد الـ Blueprint من الملف الرئيسي للـ Admin
from . import admin_bp 

# --- بروتوكول التحقق السيادي (المؤسس علي محجوب) ---
def is_admin_sovereign():
    """ يضمن السيطرة الكاملة للمؤسس فقط. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 1. عرض النافذة الأفقية الرئيسية ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers_index():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 2. محرك الاستدعاء الفوري (AJAX Fetch) ---
@admin_bp.route('/api/supplier/fetch', methods=['POST'])
@login_required
def fetch_supplier_api():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'غير مصرح'}), 403
    
    search_query = request.json.get('query')
    
    # البحث بالمعرف (963x) أو الاسم التجاري أو الهاتف
    # نقوم بإزالة '963' للبحث عن المعرف الرقمي الصافي
    clean_query = search_query.replace('963', '')
    
    supplier = Supplier.query.filter(
        (Supplier.id.like(f"%{clean_query}%")) | 
        (Supplier.trade_name.like(f"%{search_query}%")) | 
        (Supplier.phone.like(f"%{search_query}%"))
    ).first()

    if not supplier:
        return jsonify({'status': 'error', 'message': 'الكيان غير موجود في قاعدة بيانات محجوب أونلاين'}), 404

    return jsonify({
        'status': 'success',
        'data': {
            'id': supplier.id,
            'sup_id': f"SUP-MAH-963{supplier.id}",
            'wallet_id': f"WAL_MAH-963{supplier.id}",
            'trade_name': supplier.trade_name,
            'phone': supplier.phone,
            'activity': supplier.activity_type,
            'province': supplier.province,
            'tier': getattr(supplier, 'tier', 'مبتدئ'),
            'status': getattr(supplier, 'status', 'active')
        }
    })

# --- 3. محرك التحديث السيادي (AJAX Update) ---
@admin_bp.route('/api/supplier/update', methods=['POST'])
@login_required
def update_supplier_api():
    if not is_admin_sovereign():
        return jsonify({'status': 'error', 'message': 'صلاحية مرفوضة'}), 403
    
    data = request.json
    supplier = Supplier.query.get(data.get('id'))
    
    if not supplier:
        return jsonify({'status': 'error', 'message': 'فشل العثور على المورد لتحديثه'}), 404

    try:
        # تحديث البيانات الحيوية في قاعدة البيانات
        supplier.phone = data.get('phone')
        supplier.activity_type = data.get('activity')
        supplier.province = data.get('province')
        
        # تحديث الرتبة والحالة (إذا كان الموديل يدعمهما)
        if hasattr(supplier, 'tier'): supplier.tier = data.get('tier')
        if hasattr(supplier, 'status'): supplier.status = data.get('status')
        
        db.session.commit()
        return jsonify({'status': 'success', 'message': f'تم تحديث ترددات كيان "{supplier.trade_name}" بنجاح ✅'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'status': 'error', 'message': f'خطأ برمي: {str(e)}'}), 400
