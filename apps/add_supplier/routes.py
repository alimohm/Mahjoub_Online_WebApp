# coding: utf-8
import os
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for, current_app
from werkzeug.utils import secure_filename
from models.supplier_db import db, Supplier
from datetime import datetime

# تعريف المسار (Blueprint)
add_supplier_bp = Blueprint('add_supplier', __name__)

# امتدادات الملفات المسموح بها لصور الهويات
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    """التحقق من نوع الملف المرفوع"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@add_supplier_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    """المحرك الرئيسي لإضافة وتعميد الموردين"""
    
    if request.method == 'POST':
        # 1. استلام الهوية الرقمية والوصول
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
        address_detail = request.form.get('address')
        
        # 4. الربط المالي السيادي
        fin_type = request.form.get('fin_type')
        bank_name = request.form.get('bank_name')
        if bank_name == 'manual':
            bank_name = request.form.get('manual_bank_name')
        bank_acc = request.form.get('bank_acc')
        
        # 5. فئة المورد
        category = request.form.get('category')
        if category == 'manual':
            category = request.form.get('manual_category')

        # 6. معالجة رفع وأرشفة صورة الوثيقة
        file = request.files.get('identity_image')
        filename = None
        if file and allowed_file(file.filename):
            # تسمية الملف بالمعرف الموحد لسهولة التتبع
            filename = secure_filename(f"{unified_id}_{file.filename}")
            upload_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 'suppliers_docs')
            
            if not os.path.exists(upload_path):
                os.makedirs(upload_path)
            file.save(os.path.join(upload_path, filename))

        try:
            # إنشاء كائن المورد الجديد
            new_supplier = Supplier(
                sovereign_id=unified_id,
                username=username,
                trade_name=trade_name,
                owner_name=owner_name,
                identity_type=identity_type,
                identity_number=identity_number,
                identity_image=filename,
                shop_phone=shop_phone,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                province=province,
                district=district,
                address_detail=address_detail,
                activity_type=category
            )
            
            # تشفير كلمة المرور المؤقتة قبل الحفظ
            new_supplier.set_password(password)
            
            db.session.add(new_supplier)
            db.session.commit()
            
            # إذا كان الطلب AJAX (من الـ Modal)
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'status': 'success', 'message': 'تم التعميد بنجاح'}), 200
            
            flash(f'تم تعميد المورد {trade_name} بنجاح', 'success')
            return redirect(url_for('add_supplier.add_supplier'))

        except Exception as e:
            db.session.rollback()
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return jsonify({'status': 'error', 'message': str(e)}), 400
            flash(f'خطأ في النظام: {str(e)}', 'danger')

    # حساب المعرف الموحد القادم (Next ID) للعرض في الهيدر
    last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id = (last_supplier.id + 1) if last_supplier else 1
    
    return render_template('admin/add_supplier.html', next_id=next_id)

# --- محرك التحقق اللحظي (Ajax Validation Engine) ---

@add_supplier_bp.route('/admin/suppliers/check-duplicate/', methods=['GET'])
def check_duplicate():
    """محرك فحص التكرار لضمان فرادة البيانات في المنظومة"""
    check_type = request.args.get('type')
    value = request.args.get('value')
    bank_name = request.args.get('bank_name') # خاص بفحص رقم الحساب

    exists = False

    if check_type == 'username':
        exists = Supplier.query.filter_by(username=value).first() is not None
    
    elif check_type == 'trade_name':
        exists = Supplier.query.filter_by(trade_name=value).first() is not None

    elif check_type == 'shop_phone':
        exists = Supplier.query.filter_by(shop_phone=value).first() is not None

    elif check_type == 'bank_acc':
        # التحقق من أن رقم الحساب غير مسجل لنفس البنك/الشركة
        exists = Supplier.query.filter_by(bank_acc=value, bank_name=bank_name).first() is not None

    return jsonify({'exists': exists})
