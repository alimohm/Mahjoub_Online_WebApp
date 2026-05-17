# coding: utf-8
# 🔑 محرك الموردين الحوكمي والسيادي - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app, url_for
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import jinja2

# استيراد البلوبرينت المعزول الخاص بالموردين وكائن قاعدة البيانات
from . import admin_suppliers
from apps import db
from apps.models import Supplier  

def get_expected_sovereign_id():
    """
    وظيفة عرض فقط (معاينة بالواجهة): تتوقع الرقم القادم بناءً على منطق الموديل العابر للأحداث.
    النمط المعتمد: SUP-WEL-MAH963X
    """
    try:
        last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        if last_supplier and last_supplier.sovereign_id:
            try:
                parts = last_supplier.sovereign_id.split('MAH963')
                last_num = int(parts[-1])
                return f"SUP-WEL-MAH963{last_num + 1}"
            except (ValueError, IndexError):
                return f"SUP-WEL-MAH963{(last_supplier.id or 0) + 1}"
    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء معاينة المعرف المتوقع: {str(e)}")
    return "SUP-WEL-MAH9631"


@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required
def add_supplier_page():
    if request.method == 'POST':
        try:
            # 1. استقبال البيانات ومطابقتها لأعمدة الموديل الفعلي
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

            # 2. فحص أمني صارم أخير لحماية الحقول السبعة قبل الـ Commit
            check_fields = {
                "username": (Supplier.query.filter_by(username=username).first(), "اسم المستخدم (Login)"),
                "identity_number": (Supplier.query.filter_by(identity_number=identity_number).first(), "رقم الوثيقة / الهوية"),
                "owner_name": (Supplier.query.filter_by(owner_name=owner_name).first(), "اسم المالك الكامل"),
                "trade_name": (Supplier.query.filter_by(trade_name=trade_name).first(), "الاسم التجاري للمنشأة"),
                "owner_phone": (Supplier.query.filter_by(owner_phone=owner_phone).first(), "رقم هاتف المالك"),
                "shop_phone": (Supplier.query.filter_by(shop_phone=shop_phone).first(), "هاتف المنشأة (محل)"),
                "bank_acc": (Supplier.query.filter_by(bank_acc=bank_acc).first(), "رقم الحساب")
            }

            for key, (exists, field_title) in check_fields.items():
                if exists:
                    return jsonify({
                        "status": "error",
                        "message": f"عذراً، حقل ({field_title}) مسجل مسبقاً في المنصة ومحفوظ!"
                    }), 400

            # 3. تشفير كلمة المرور وبناء كائن المورد متوافقاً مع أسماء أعمدة الموديل
            hashed_password = generate_password_hash(password)
            
            new_supplier = Supplier(
                username=username,
                password_hash=hashed_password,  # تم التعديل لتطابق اسم العمود بالموديل password_hash
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
                activity_type=activity_type,
                registration_source='لوحة التحكم', # تم التوليد عبر الإدارة
                created_by_id=current_user.id if hasattr(current_user, 'id') else None
            )

            # معالجة صورة الوثيقة الرمزية إن وجدت
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '':
                    # new_supplier.identity_image = secure_filename(file.filename)
                    pass

            # 4. الحفظ في قاعدة البيانات (سيتكفل الموديل بتوليد sovereign_id عبر الـ Event تلقائياً)
            db.session.add(new_supplier)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "تم تعميد المورد بنجاح وحفظه بنيوياً في قاعدة البيانات.",
                "data": {
                    "username": new_supplier.username,
                    "sovereign_id": new_supplier.sovereign_id  # تم سحبه بعد الـ commit بنجاح
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ أثناء حفظ المورد في قاعدة البيانات: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"خطأ في معالجة قاعدة البيانات: {str(e)}"
            }), 500

    # مرحلة الـ GET لعرض الصفحة
    sovereign_id = get_expected_sovereign_id()
    
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
    الفحص الفوري واللحظي الصارم عبر السيرفر للحقول السبعة المطلوبة لمنع التكرار البنيوي.
    إذا كانت القيمة موجودة مسبقاً ترجع الاستجابة True لتظهر علامة (X) الحمراء في الواجهة فوراً.
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    
    if not check_type or not value:
        return jsonify({"exists": False, "error": "Missing parameters"}), 400
        
    exists = False
    try:
        # هنا تم مطابقة شروط الـ IF لتطابق أسماء الحقول السبعة بدقة متناهية
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
            
        else:
            current_app.logger.warning(f"⚠️ نوع فحص غير مدعوم في النظام: {check_type}")

    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء الاستعلام عن حقل [{check_type}] في الداتابيز: {str(e)}")
        return jsonify({"exists": False, "error": "Database error"}), 500
        
    # إرجاع النتيجة للـ الجافاسكربت (إذا وجد الحقل سيرسل true وتتحول العلامة إلى X تلقائياً)
    return jsonify({"exists": exists})
