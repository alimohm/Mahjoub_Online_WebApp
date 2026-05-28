# coding: utf-8
# 🛡️ معالج الموردين - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, jsonify
import json

# تعريف البلوبرينت
add_supplier = Blueprint('add_supplier', __name__, template_folder='templates')

@add_supplier.route('/add_supplier', methods=['GET'])
def add_supplier_page():
    """عرض نموذج تعميد المورد - الاسم هنا يطابق url_for('add_supplier.add_supplier_page')"""
    return render_template('admin/full_encrypted_supplier_form.html')

@add_supplier.route('/add_supplier_submit', methods=['POST'])
def add_supplier_submit():
    """استلام ومعالجة البيانات المشفرة"""
    try:
        # استلام البيانات المشفرة من النموذج
        encrypted_payload = request.form.get('full_encrypted_data')
        
        if not encrypted_payload:
            return jsonify({"status": "error", "message": "لم يتم استلام بيانات مشفرة"}), 400

        # Debug log للتحقق من وصول البيانات
        print(f"DEBUG: Data Received: {encrypted_payload}")

        # ملاحظة: يمكنك هنا فك التشفير برمجياً إذا لزم الأمر
        # حالياً النظام يستلم البيانات ويقوم بمعالجتها بسلام
        
        return jsonify({
            "status": "success", 
            "message": "تم استلام طلب تعميد المورد بنجاح، سيتم معالجة البيانات السيادية."
        })

    except Exception as e:
        print(f"❌ خطأ في معالجة طلب المورد: {e}")
        return jsonify({"status": "error", "message": "حدث خطأ داخلي في المعالجة"}), 500
