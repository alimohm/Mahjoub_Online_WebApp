# coding: utf-8
# 🔑 محرك الموردين الحوكمي والسيادي - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import jinja2

# استيراد البلوبرينت المعزول الخاص بالموردين
from . import admin_suppliers
# استيراد كائن قاعدة البيانات والموديل الفعلي للموردين
from apps import db
from apps.models import Supplier  

def generate_sovereign_id():
    """
    سحب آخر رقم مورد من قاعدة البيانات وزيادة العداد بمقدار 1 تلقائياً ليكون المعرف القادم دقيقاً.
    النمط المعتمد والثابت بالداتابيز: SUP-WEL-MAH963
    """
    prefix = "SUP-WEL-MAH963"
    default_id = f"{prefix}19"
    
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        
        if last_supplier and last_supplier.sovereign_id:
            last_code = last_supplier.sovereign_id.strip()
            if last_code.startswith(prefix):
                num_part_str = last_code.replace(prefix, "")
                if num_part_str.isdigit():
                    next_num = int(num_part_str) + 1
                    return f"{prefix}{next_num}"
    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء احتساب الرقم الحوكمي التالي: {str(e)}")
    
    return default_id


# ضبط الـ endpoint ليدعم الاسمين معاً لمنع خطأ الـ BuildError تماماً أثناء المزامنة على Railway
@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required
def add_supplier_page():
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات السبعة الأساسية وبقية الحقول من الفورم
            username = request.form.get('username', '').strip()
            password = request.form.get('password', '').strip()
            identity_type = request.form.get('identity_type', '').strip()
            identity_number = request.form.get('identity_number', '').strip()
            owner_name = request.form.get('owner_name', '').strip()
            trade_name = request.form.get('trade_name', '').strip()
            owner_phone = request.form.get('owner_phone', '').strip()
            shop_phone = request.form.get('shop_phone', '').strip()
            province = request.form.get('province', '').strip()
            district = request.form.get('district', '').strip()
            address_detail = request.form.get('address_detail', '').strip()
            fin_type = request.form.get('fin_type', '').strip()
            bank_name = request.form.get('bank_name', '').strip()
            bank_acc = request.form.get('bank_acc', '').strip()
            activity_type = request.form.get('activity_type', '').strip()
            
            # توليد المعرف السيادي بشكل آمن وصارم لمنع أي تلاعب أو تكرار
            sovereign_id = generate_sovereign_id()

            # 2. فحص أمني أخير للتأكد من عدم وجود تكرار قبل الحفظ الفعلي
            check_fields = {
                "اسم المستخدم": Supplier.query.filter_by(username=username).first(),
                "رقم الوثيقة": Supplier.query.filter_by(identity_number=identity_number).first(),
                "اسم المالك": Supplier.query.filter_by(owner_name=owner_name).first(),
                "الاسم التجاري": Supplier.query.filter_by(trade_name=trade_name).first(),
                "هاتف المالك": Supplier.query.filter_by(owner_phone=owner_phone).first(),
                "هاتف المنشأة": Supplier.query.filter_by(shop_phone=shop_phone).first(),
                "رقم الحساب": Supplier.query.filter_by(bank_acc=bank_acc).first()
            }
            
            for field_title, exists in check_fields.items():
                if exists:
                    return jsonify({
                        "status": "error",
                        "message": f"عذراً، حقل ({field_title}) مسجل مسبقاً في النظام ولا يمكن تكراره."
                    }), 400

            # 3. تشفير كلمة المرور وتجهيز الكائن للحفظ
            hashed_password = generate_password_hash(password)
            
            new_supplier = Supplier(
                sovereign_id=sovereign_id,
                username=username,
                password=hashed_password,
                identity_type=identity_type,
                identity_number=identity_number,
                owner_name=owner_name,
                trade_name=trade_name,
                owner_phone=owner_phone,
                shop_phone=shop_phone,
                province=province,
                district=district,
                address_detail=address_detail,
                fin_type=fin_type,
                bank_name=bank_name,
                bank_acc=bank_acc,
                activity_type=activity_type
            )

            # التعامل مع الملفات المرفوعة (صورة الوثيقة) إن وجدت
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '':
                    # هنا يمكنك تضمين دالة الحفظ الخاصة بك مثل: save_file(file)
                    # new_supplier.identity_image = secure_filename(file.filename)
                    pass

            # 4. تعميد الحفظ النهائي في قاعدة البيانات
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "تم تعميد المورد وحفظه في قاعدة البيانات الحوكمية بنجاح.",
                "data": {
                    "username": username, 
                    "sovereign_id": sovereign_id
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ أثناء حفظ المورد في الداتابيز: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"حدث خطأ داخلي أثناء معالجة البيانات: {str(e)}"
            }), 500

    # عرض الصفحة (GET)
    sovereign_id = generate_sovereign_id()
    
    # تأمين إرسال متغيرات فارغة لـ CSRF لتجنب الانهيار إذا لم تكن الإضافة مثبتة في بيئة معينة
    csrf_val = ""
    try:
        if 'csrf' in current_app.extensions:
            from flask_wtf.csrf import generate_csrf
            csrf_val = generate_csrf()
    except Exception:
        pass

    try:
        return render_template('admin/add_supplier.html', sovereign_id=sovereign_id, owner=current_user, backup_csrf=csrf_val)
    except jinja2.exceptions.TemplateNotFound:
        return render_template('add_supplier.html', sovereign_id=sovereign_id, owner=current_user, backup_csrf=csrf_val)


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    الفحص الفوري واللحظي عبر قاعدة البيانات للحقول السبعة لمنع التكرار البنيوي في المنصة.
    إذا كانت القيمة موجودة مسبقاً ترجع (exists: true) لتظهر إشارة الخطر (X) في الواجهة فوراً.
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    
    if not check_type or not value:
        return jsonify({"exists": False, "error": "Missing parameters"}), 400
        
    exists = False
    try:
        # ربط شروط الفحص للحقول السبعة مباشرة بالموديل (Supplier) والتحقق من التكرار
        if check_type == 'username':
            exists = Supplier.query.filter_by(username=value).first() is not None
            
        elif check_type == 'identity_number':
            exists = Supplier.query.filter_by(identity_number=value).first() is not None
            
        elif check_type == 'owner_name':
            exists = Supplier.query.filter_by(owner_name=value).first() is not None
            
        elif check_type == 'trade_name':
            exists = Supplier.query.filter_by(trade_name=value).first() is not None
            
        elif check_type == 'owner_phone':
            exists = Supplier.query.filter_by(owner_phone=value).first() is not None
            
        elif check_type == 'shop_phone':
            exists = Supplier.query.filter_by(shop_phone=value).first() is not None
            
        elif check_type == 'bank_acc':
            exists = Supplier.query.filter_by(bank_acc=value).first() is not None

    except Exception as e:
        current_app.logger.error(f"❌ خطأ في فحص التكرار اللحظي داخل قاعدة البيانات للحقل {check_type}: {str(e)}")
        return jsonify({"exists": False, "error": "Database query error"}), 500
        
    return jsonify({"exists": exists})
