from flask import Blueprint, render_template, request, jsonify
from datetime import datetime
# استيراد الموديل من المسار الجديد الذي حددته
from models.supplier_db import db, Supplier 

admin_suppliers = Blueprint('admin_suppliers', __name__)

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استلام المعرف السيادي والبيانات الأساسية
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            # معالجة الفئة (يدوي أو اختيار)
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            # 2. بيانات المالك والمنشأة
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            
            # 3. بيانات الموقع (العنوان)
            province = request.form.get('province')
            district = request.form.get('district')
            # استخدام address_detail بناءً على ملاحظتك وتحديث القالب
            address_detail = request.form.get('address_detail')

            # 4. الربط المالي السيادي
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            bank_acc = request.form.get('bank_acc')

            # 5. إنشاء سجل المورد الجديد
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password,
                category=category,
                owner_name=owner_name,
                trade_name=trade_name,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                finance_type=fin_type,
                bank_name=bank_name,
                bank_account=bank_acc,
                created_at=datetime.utcnow()
            )

            db.session.add(new_supplier)
            db.session.commit()

            # 6. إرجاع استجابة النجاح للنموذج (JSON)
            # تم ضبط المفاتيح لتطابق المعرفات في الجافاسكريبت (res_sovereign_id, res_username...)
            return jsonify({
                'status': 'success',
                'data': {
                    'sovereign_id': unified_id,
                    'username': username,
                    'password': password
                }
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                'status': 'error',
                'message': f'حدث خطأ في محرك الحفظ: {str(e)}'
            }), 400

    # في حالة GET: حساب المعرف التالي SUP-WEL-MAH963 + X
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id = (last_supplier.id + 1) if last_supplier else 1
    except:
        next_id = 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)
