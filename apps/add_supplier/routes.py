import os
from flask import Blueprint, render_template, request, jsonify, current_app
from datetime import datetime
from werkzeug.utils import secure_filename

# استيراد قاعدة البيانات والموديل من المسار الصحيح
from models.supplier_db import db, Supplier 

# تعريف الـ Blueprint مع حل مشكلة المسار التي ظهرت في image_955a54.png
admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder='../../templates' # يوجه الفلاسك لمجلد القوالب الرئيسي
)

@admin_suppliers.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استلام البيانات الأساسية (المعرف الموحد والوصول)
            unified_id = request.form.get('unified_id')
            username = request.form.get('username')
            password = request.form.get('password')
            
            # معالجة فئة المورد (الاختيار أو الإدخال اليدوي)
            category = request.form.get('category')
            if category == 'manual':
                category = request.form.get('manual_category')

            # 2. بيانات المالك والمنشأة والاتصال
            owner_name = request.form.get('owner_name')
            trade_name = request.form.get('trade_name')
            shop_phone = request.form.get('shop_phone')
            owner_phone = request.form.get('owner_phone') # حقل المالك الجديد
            
            # 3. بيانات الموقع الجغرافي
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail', '')

            # 4. بيانات الربط المالي (معالجة الإدخال اليدوي للبنك/الصرافة)
            fin_type = request.form.get('fin_type')
            bank_name = request.form.get('bank_name')
            manual_bank = request.form.get('manual_bank_name')
            # إذا لم يتم اختيار بنك من القائمة وتم كتابته يدوياً
            final_bank_name = manual_bank if (not bank_name or bank_name == "") else bank_name
            
            bank_acc = request.form.get('bank_acc')

            # 5. معالجة الرفع (صورة الوثيقة)
            identity_image = request.files.get('identity_image')
            image_filename = None
            if identity_image and identity_image.filename != '':
                image_filename = secure_filename(f"{unified_id}_{identity_image.filename}")
                # يتم الحفظ في مجلد الرفع المحدد في إعدادات التطبيق
                # upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_filename)
                # identity_image.save(upload_path)

            # 6. إنشاء سجل المورد في قاعدة بيانات "محجوب أونلاين"
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                password=password, 
                category=category,
                owner_name=owner_name,
                trade_name=trade_name,
                shop_phone=shop_phone,
                owner_phone=owner_phone, # تأكد من وجود هذا العمود في الموديل
                province=province,
                district=district,
                address_detail=address_detail,
                finance_type=fin_type,
                bank_name=final_bank_name,
                bank_account=bank_acc,
                identity_image=image_filename,
                created_at=datetime.utcnow()
            )

            db.session.add(new_supplier)
            db.session.commit()

            # الاستجابة لـ JavaScript (SweetAlert2)
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
                'message': f'فشل النظام في تعميد البيانات: {str(e)}'
            }), 400

    # في حالة GET: جلب الرقم التسلسلي للمورد القادم
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id_num = (last_supplier.id + 1) if last_supplier else 1
    except:
        next_id_num = 1
        
    return render_template('admin/add_supplier.html', next_id=next_id_num)

@admin_suppliers.route('/admin/suppliers/check-validate', methods=['GET'])
def check_validate():
    """محرك فحص البيانات لمنع التكرار (يستخدمه الـ AJAX في الواجهة)"""
    val_type = request.args.get('type')
    value = request.args.get('value')
    
    if not value: return jsonify({'exists': False})
    
    # البحث الديناميكي في قاعدة البيانات
    exists = False
    if val_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    elif val_type == 'shop_phone':
        exists = Supplier.query.filter_by(shop_phone=value).first() is not None
        
    return jsonify({'exists': exists})
