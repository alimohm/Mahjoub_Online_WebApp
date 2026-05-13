from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify, session
from models.supplier_db import db, Supplier  
from datetime import datetime
from functools import wraps

admin_suppliers = Blueprint('admin_suppliers', __name__, template_folder='templates')

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return jsonify({"status": "error", "message": "يجب تسجيل الدخول أولاً"}), 401
        return f(*args, **kwargs)
    return decorated_function

@admin_suppliers.route('/add-supplier', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        # استقبال البيانات سواء كانت JSON (من الـ Fetch) أو Form عادية
        data = request.get_json() if request.is_json else request.form

        try:
            # استخراج البيانات بناءً على الأسماء الموجودة في نموذجك الجديد
            new_supplier = Supplier(
                name=data.get('username'), # اسم المستخدم للدخول
                trade_name=data.get('trade_name'), # الاسم التجاري
                owner=data.get('owner_name'), # اسم المالك
                region=data.get('province') + " - " + data.get('district'), # النطاق الجغرافي
                contact=data.get('phone'),
                category=data.get('activity_type'),
                bank_info=f"{data.get('bank_name')} : {data.get('bank_acc')}", # المحفظة السيادية
                created_at=datetime.utcnow()
            )
            
            db.session.add(new_supplier)
            db.session.commit()
            
            return jsonify({
                "status": "success", 
                "message": f"تم تعميد المورد {data.get('trade_name')} بنجاح في النظام السيادي."
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"خطأ تقني: {str(e)}"}), 500

    # عرض الواجهة (GET)
    return render_template('admin/add_supplier.html', next_id=963) # تأكد من تمرير next_id
