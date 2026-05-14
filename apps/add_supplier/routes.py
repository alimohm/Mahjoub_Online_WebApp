import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from apps.models import db, Supplier  # تأكد من مطابقة المسارات في مشروعك
from apps.utils import admin_required 

add_supplier_bp = Blueprint('add_supplier', __name__)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_supplier_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
@admin_required
def add_supplier():
    if request.method == 'POST':
        # 1. استلام البيانات الأساسية
        unified_id = request.form.get('unified_id')
        username = request.form.get('username')
        password = request.form.get('password')
        
        # 2. معالجة بيانات الهوية (اختيار أو يدوي)
        identity_type = request.form.get('identity_type')
        if identity_type == 'manual':
            identity_type = request.form.get('manual_identity_type')
        identity_number = request.form.get('identity_number')
        
        # 3. بيانات المالك والمنشأة
        owner_name = request.form.get('owner_name')
        trade_name = request.form.get('trade_name')
        shop_phone = request.form.get('shop_phone')
        province = request.form.get('province')
        district = request.form.get('district')
        address = request.form.get('address')
        
        # 4. الربط المالي (اختيار أو يدوي)
        fin_type = request.form.get('fin_type')
        bank_name = request.form.get('bank_name')
        if bank_name == 'manual':
            bank_name = request.form.get('manual_bank_name')
        bank_acc = request.form.get('bank_acc')
        
        # 5. فئة المورد (اختيار أو يدوي)
        category = request.form.get('category')
        if category == 'manual':
            category = request.form.get('manual_category')

        # 6. معالجة رفع صورة الوثيقة
        file = request.files.get('identity_image')
        filename = None
        if file and allowed_file(file.filename):
            # تأمين الاسم وحمايته من الثغرات
            clean_filename = secure_filename(file.filename)
            filename = f"{unified_id}_{clean_filename}"
            
            upload_path = os.path.join(current_app.config.get('UPLOAD_FOLDER', 'uploads'), 'suppliers_ids')
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))

        try:
            # إنشاء سجل المورد الجديد
            new_supplier = Supplier(
                unified_id=unified_id,
                username=username,
                identity_type=identity_type,
                identity_number=identity_number,
                identity_image=filename,
                owner_name=owner_name,
                trade_name=trade_name,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address=address,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                category=category
            )
            
            # تشفير كلمة المرور (تأكد أن الدالة موجودة داخل الـ Model)
            if hasattr(new_supplier, 'set_password'):
                new_supplier.set_password(password)
            else:
                new_supplier.password = password # حماية مؤقتة إذا لم تكن الدالة مشفرة بعد
            
            db.session.add(new_supplier)
            db.session.commit()
            
            flash(f'تم اعتماد المورد {trade_name} بنجاح بالمعرف {unified_id}', 'success')
            
            # تغيير التوجيه إلى دالة العرض الحالية لتجنب الـ BuildError مؤقتاً
            return redirect(url_for('add_supplier.add_supplier'))

        except Exception as e:
            db.session.rollback()
            flash(f'حدث خطأ أثناء الحفظ في قاعدة البيانات: {str(e)}', 'danger')

    # الطريقة الاحترافية والآمنة لحساب المعرف القادم دون حدوث خطأ كراش
    try:
        max_id = db.session.query(db.func.max(Supplier.id)).scalar()
        next_id = (max_id + 1) if max_id else 1
    except Exception:
        next_id = 1
    
    # تأكد من أن ملف الـ HTML يقع في هذا المسار تماماً داخل مجلد templates
    return render_template('admin/add_supplier.html', next_id=next_id)


# --- نظام التحقق اللحظي المصحح (Ajax Validation) ---

@add_supplier_bp.route('/admin/suppliers/check-duplicate', methods=['GET'])
@admin_required
def check_duplicate():
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    bank_name = request.args.get('bank_name', '').strip()

    if not check_type or not value:
        return jsonify({'exists': False})

    exists = False

    if check_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    
    elif check_type == 'trade_name':
        exists = Supplier.query.filter_by(trade_name=value).first() is not None

    elif check_type == 'shop_phone':
        exists = Supplier.query.filter_by(shop_phone=value).first() is not None

    elif check_type == 'bank_acc':
        # التحقق الذكي لمنع تكرار الحساب لنفس البنك
        exists = Supplier.query.filter_by(bank_acc=value, bank_name=bank_name).first() is not None

    return jsonify({'exists': exists})
