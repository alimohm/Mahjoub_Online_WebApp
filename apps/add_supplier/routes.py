# coding: utf-8
import os
from flask import Blueprint, render_template, request, jsonify
from flask_login import login_required
from datetime import datetime
from werkzeug.security import generate_password_hash

# استيراد قاعدة البيانات والموديل
from apps import db  
from apps.models.supplier_db import Supplier 

current_dir = os.path.dirname(os.path.abspath(__file__))
# تأكد من أن المسار يشير إلى مجلد templates داخل المديول
template_path = os.path.join(current_dir, 'templates')

admin_suppliers = Blueprint(
    'admin_suppliers', 
    __name__,
    template_folder=template_path
)

@admin_suppliers.route('/add', methods=['GET', 'POST'])
@login_required 
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات الأساسية
            username = request.form.get('username', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            password = request.form.get('password')

            # 2. التحقق من عدم تكرار البيانات الحساسة
            if Supplier.query.filter_by(username=username).first():
                return jsonify({'status': 'error', 'message': 'اسم المستخدم مسجل مسبقاً في النظام!'}), 400

            # 3. معالجة حقول "الإدخال اليدوي" الديناميكية
            # يتم استقبال القيمة من الـ Select مباشرة لأن JS يقوم بتحديثها لحظياً
            
            # أ) نوع الهوية
            identity_type = request.form.get('identity_type')
            
            # ب) جهة التحويل المالي (البنك أو الشركة)
            bank_name = request.form.get('bank_name')

            # ج) فئة المورد
            category = request.form.get('category', '').strip()

            # 4. تشفير كلمة المرور وإنشاء سجل المورد الجديد
            hashed_pw = generate_password_hash(password)
            
            new_supplier = Supplier(
                sovereign_id=request.form.get('unified_id'), # المعرف الموحد المرسل من الفورم
                username=username,
                password_hash=hashed_pw,
                identity_type=identity_type,
                identity_number=request.form.get('identity_number', '').strip(),
                activity_type=category,
                owner_name=request.form.get('owner_name', '').strip(),
                trade_name=trade_name,
                shop_phone=request.form.get('shop_phone', '').strip(),
                owner_phone=request.form.get('owner_phone', '').strip(),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address'),
                fin_type=request.form.get('fin_type'),
                bank_name=bank_name,
                bank_acc=request.form.get('bank_acc', '').strip(),
                created_at=datetime.utcnow()
            )

            # 5. معالجة الصورة (اختياري - يتم تفعيل المسار حسب إعدادات السيرفر لديك)
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '':
                    # هنا يمكن إضافة منطق رفع الصور (على سبيل المثال S3 أو Local Storage)
                    pass

            # 6. الحفظ النهائي في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()

            # إرجاع استجابة نجاح ليقوم الـ Frontend بإظهار الـ Modal
            return jsonify({
                'status': 'success',
                'message': 'تم تعميد المورد بنجاح في نظام الأرشفة السيادي',
                'data': {
                    'username': username,
                    'unified_id': request.form.get('unified_id')
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({'status': 'error', 'message': f'فشل في عملية التعميد: {str(e)}'}), 500

    # حساب المعرف التالي (Next ID) لعرضه في واجهة الـ GET
    try:
        last_s = Supplier.query.order_by(Supplier.id.desc()).first()
        next_id = (last_s.id + 1) if last_s else 1
    except:
        next_id = 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)

# API للتحقق اللحظي (Check as you type)
@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    # خريطة الحقول المسموح بالتحقق منها
    field_map = {
        'username': Supplier.username,
        'trade_name': Supplier.trade_name,
        'shop_phone': Supplier.shop_phone,
        'identity_number': Supplier.identity_number
    }

    target_field = field_map.get(check_type)
    exists = False
    
    if target_field:
        exists = Supplier.query.filter(target_field == value).first() is not None

    return jsonify({'exists': exists})
