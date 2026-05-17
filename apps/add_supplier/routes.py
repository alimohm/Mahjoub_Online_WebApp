# coding: utf-8
# 🔑 محرك الموردين المعزول - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
import jinja2
import secrets

# استيراد البلوبرينت المعزول الخاص بالموردين
from . import admin_suppliers

def generate_sovereign_id():
    """توليد معرف سيادي فريد للمورد الجديد لمنع التكرار البنيوي"""
    return f"MS-{secrets.randbelow(900000) + 100000}"


@admin_suppliers.route('/add', methods=['GET', 'POST'])
@login_required  # درع الحماية والنفاذ السيادي للمنصة
def add_supplier_page():
    """
    إدارة وتعميد الشركاء (الموردين) الجدد.
    تم تغيير اسم الدالة إلى add_supplier_page لمنع أي Endpoint Conflict 
    مع لوحة التحكم المركزية وسرعة التقاطها ديناميكياً.
    """
    if request.method == 'POST':
        # استقبال البيانات القادمة من الحوكمة الرقمية للواجهة
        username = request.form.get('username')
        sovereign_id = request.form.get('sovereign_id')
        trade_name = request.form.get('trade_name')
        owner_phone = request.form.get('owner_phone')
        
        # 💡 [ملاحظة هندسية]: هنا يتم وضع منطق الحفظ في قاعدة البيانات (DB) الخاص بك
        # مثال: new_supplier = Supplier(username=username, sovereign_id=sovereign_id, ...)
        
        current_app.logger.info(f"✨ تم اعتماد شريك جديد بنجاح: {trade_name} ({sovereign_id})")
        
        # إرجاع استجابة JSON نقية لتستقبلها دالة الفيتش (Fetch) في الواجهة وتفتح مودال النجاح
        return jsonify({
            "status": "success",
            "message": "تم تعميد المورد بنجاح في النظام الحوكمي الموحد.",
            "data": {
                "username": username, 
                "sovereign_id": sovereign_id
            }
        }), 200

    # في حالة طلب الصفحة عبر GET: توليد المعرف برمجياً وعرض الواجهة
    sovereign_id = generate_sovereign_id()
    
    # موازنة المسارات لضمان رندرة القالب سواء كان معزولاً أو في النطاق المباشر منعاً للـ TemplateNotFound
    try:
        return render_template('admin/add_supplier.html', sovereign_id=sovereign_id, owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        current_app.logger.warning("تنبيه: تم موازنة مسار قالب add_supplier إلى المسار المباشر.")
        return render_template('add_supplier.html', sovereign_id=sovereign_id, owner=current_user)


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    الفحص الفوري للبيانات عبر السيرفر (الاسم، الجوال، الحساب البنكي)
    لمنع التكرار الرقمي وتأمين الحوكمة المالية قبل الحفظ الكلي.
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    
    if not check_type or not value:
        return jsonify({"exists": False, "error": "Missing parameters"}), 400
        
    # 💡 [ملاحظة هندسية]: استعلم من الداتابيز هنا لمنع التكرار
    # مثال: exists = Supplier.query.filter_by(**{check_type: value}).first() is not None
    exists = False 
    
    return jsonify({"exists": exists})
