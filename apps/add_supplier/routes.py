# coding: utf-8
# 🔑 محرك حوكمة الموردين والربط المالي السيادي لعام 2026 - منصة محجوب أونلاين

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash
import random

# استيراد البلوبرينت وكائن قاعدة البيانات المركزي والنماذج النواة
from . import admin_suppliers
from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet

@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@login_required
def add_supplier_page():
    """
    مسار تعميد الموردين وإنشاء المحافظ المالية المشفرة تلقائياً في السيرفر الحي
    """
    if request.method == 'POST':
        try:
            # 1. استقبال الحقول والنوايا الحوكمية من الواجهة الأمامية
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

            # 🛠️ لقط المعرفات السيادية الثابتة والمطلوبة من الواجهة لمنع تعارض قيد Not-Null
            sovereign_id = request.form.get('sovereign_id', 'SUP-MAH9631').strip()
            wallet_code = request.form.get('wallet_code', 'WEL-MAH9631').strip()

            # فرض الرتبة والحالة الحركية للنظام تلقائياً
            user_rank = 'سيادي'
            system_status = 'active'

            # فحص المدخلات الحرجة لضمان سلامة النواة
            if not username or not password or not owner_name:
                return jsonify({"status": "error", "message": "تنبيه حوكمي: حقول الوصول الأساسية مطلوبة."}), 400

            # 2. فحص التكرار لمنع تضارب المسارات في Postgres
            exists = db.session.query(Supplier.id).filter_by(username=username).first()
            if exists:
                return jsonify({"status": "error", "message": "اسم المستخدم هذا مسجل مسبقاً في النظام."}), 400

            # 3. تشفير كلمة المرور وتشييد كائن المورد
            hashed_password = generate_password_hash(password)
            new_supplier = Supplier(
                username=username,
                password_hash=hashed_password,
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
                registration_source='لوحة التحكم',
                rank_grade=user_rank,         
                status=system_status,         
                created_by_id=current_user.id if hasattr(current_user, 'id') else None
            )

            db.session.add(new_supplier)
            db.session.flush()  # حجز المعرف التسلسلي (ID) للمورد حياً دون إغلاق المعاملة المفتوحة

            # 4. 💳 التشييد الآمن للمحفظة المالية وحقن الكود المتوافق والجاهز للحفظ
            new_wallet = SupplierWallet(
                supplier_id=new_supplier.id,
                wallet_code=wallet_code  # تخزين القيمة "WEL-MAH9631" رسمياً لكسر الـ Constraint
            )
            db.session.add(new_wallet)
            
            # تثبيت الحفظ النهائي للمعاملة المزدوجة بنجاح تام
            db.session.commit() 

            return jsonify({
                "status": "success",
                "message": "تم تعميد المورد بنجاح وتوليد محفظته السيادية المحددة حياً.",
                "data": {
                    "username": username,
                    "sovereign_id": sovereign_id,
                    "wallet_code": wallet_code
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ بنيوي حرج أثناء حفظ المورد: {str(e)}")
            return jsonify({
                "status": "error",
                "message": f"بنية السيرفر ترفض الحفظ: {str(e)}"
            }), 500

    # 5. معالجة مرحلة العرض اللحظي (GET)
    backup_csrf_token = ""
    try:
        if 'csrf' in current_app.extensions:
            from flask_wtf.csrf import generate_csrf
            backup_csrf_token = generate_csrf()
    except Exception:
        pass

    return render_template(
        'admin/add_supplier.html', 
        sovereign_id="SUP-MAH9631", 
        owner=current_user, 
        backup_csrf=backup_csrf_token
    )


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    محرك الاستعلام والتحقق المباشر من الواجهة لمنع تكرار البيانات الفريدة (اسم المستخدم، رقم الوثيقة، الحساب المالي)
    """
    check_type = request.args.get('type', '').strip()
    value = request.args.get('value', '').strip()

    if not check_type or not value:
        return jsonify({"exists": False}), 400

    exists = False
    try:
        if check_type == 'username':
            exists = db.session.query(Supplier.id).filter_by(username=value).first() is not None
        elif check_type == 'identity_number':
            exists = db.session.query(Supplier.id).filter_by(identity_number=value).first() is not None
        elif check_type == 'bank_acc':
            exists = db.session.query(Supplier.id).filter_by(bank_acc=value).first() is not None
        elif check_type == 'owner_phone':
            exists = db.session.query(Supplier.id).filter_by(owner_phone=value).first() is not None
        elif check_type == 'shop_phone':
            exists = db.session.query(Supplier.id).filter_by(shop_phone=value).first() is not None
        elif check_type == 'trade_name':
            exists = db.session.query(Supplier.id).filter_by(trade_name=value).first() is not None
        elif check_type == 'owner_name':
            exists = db.session.query(Supplier.id).filter_by(owner_name=value).first() is not None
    except Exception as e:
        current_app.logger.error(f"Error checking duplicate: {e}")
        return jsonify({"exists": False, "error": str(e)}), 500

    return jsonify({"exists": exists}), 200
