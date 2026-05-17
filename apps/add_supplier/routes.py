# coding: utf-8
# 🔑 محرك الموردين السيادي والمطور - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
import jinja2

# استيراد البلوبرينت المعزول الخاص بالموردين
from . import admin_suppliers
# 💡 تأكد من إلغاء تعليق وتعديل السطر أدناه لاستيراد الموديل الحقيقي لقاعدة البيانات لديك
# from apps.models import Supplier  

def generate_sovereign_id():
    """
    سحب آخر رقم مورد من قاعدة البيانات وزيادة العداد المتغير بمقدار 1 تلقائياً.
    النمط المعتمد: الثابت هو SUP-WEL-MAH963 والمتغير هو الخانات الرقمية الأخيرة (مثل 18 -> 19).
    """
    prefix = "SUP-WEL-MAH963"
    default_id = f"{prefix}19"  # القيمة الافتراضية التالية بعد الرقم 18 الظاهر في قاعدتك
    
    try:
        # 💡 استعلام جلب آخر مورد مضاف لقاعدة البيانات بناءً على المعرف التلقائي
        # last_supplier = Supplier.query.order_by(Supplier.id.desc()).first()
        last_supplier = None  # (قم بإلغاء تعليق السطر الأعلى عند ربطه بالموديل الفعلي)
        
        if last_supplier and last_supplier.sovereign_id:
            last_code = last_supplier.sovereign_id.strip()
            
            # التحقق من أن الكود يبدأ بالجزء الثابت المعتمد
            if last_code.startswith(prefix):
                # استخراج الجزء الرقمي المتغير (ما بعد الـ 963)
                num_part_str = last_code.replace(prefix, "")
                if num_part_str.isdigit():
                    next_num = int(num_part_str) + 1
                    # إرجاع المعرف الجديد مدمجاً مع الجزء الثابت لحفظ التناسق البنيوي
                    return f"{prefix}{next_num}"
    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء احتساب الرقم الحوكمي التالي: {str(e)}")
    
    return default_id


@admin_suppliers.route('/add', methods=['GET', 'POST'], endpoint='add_supplier_page')
@admin_suppliers.route('/add_legacy', methods=['GET', 'POST'], endpoint='add_supplier')
@login_required  # درع النفاذ وتأمين الحوكمة الرقمية للمنصة
def add_supplier_page():
    """
    إدارة وتعميد الشركاء (الموردين) الجدد.
    تدعم الـ Endpoints القديمة والجديدة معاً لمنع أخطاء الـ BuildError في الـ Jinja2.
    """
    if request.method == 'POST':
        # استقبال البيانات القادمة من استمارة الحوكمة الرقمية للواجهة
        username = request.form.get('username')
        sovereign_id = request.form.get('sovereign_id')
        trade_name = request.form.get('trade_name')
        owner_phone = request.form.get('owner_phone')
        
        # 💡 هنا يتم وضع منطق الحفظ في قاعدة البيانات (DB) الخاص بك
        # مثال:
        # new_supplier = Supplier(username=username, sovereign_id=sovereign_id, trade_name=trade_name, owner_phone=owner_phone)
        # db.session.add(new_supplier)
        # db.session.commit()
        
        current_app.logger.info(f"✨ تم اعتماد شريك جديد بنجاح: {trade_name} ({sovereign_id})")
        
        # إرجاع استجابة JSON نقية لتستقبلها دالة الـ Fetch في الفرونتيند وتفتح مودال النجاح
        return jsonify({
            "status": "success",
            "message": "تم تعميد المورد بنجاح في النظام الحوكمي الموحد.",
            "data": {
                "username": username, 
                "sovereign_id": sovereign_id
            }
        }), 200

    # في حالة طلب الصفحة عبر GET: توليد المعرف برمجياً بناءً على آخر رقم في القاعدة + 1
    sovereign_id = generate_sovereign_id()
    
    # موازنة المسارات لضمان رندرة القالب في بيئة Railway دون مشاكل TemplateNotFound
    try:
        return render_template('admin/add_supplier.html', sovereign_id=sovereign_id, owner=current_user)
    except jinja2.exceptions.TemplateNotFound:
        current_app.logger.warning("تنبيه: تم موازنة مسار قالب add_supplier إلى المسار المباشر.")
        return render_template('add_supplier.html', sovereign_id=sovereign_id, owner=current_user)


@admin_suppliers.route('/check-duplicate', methods=['GET'])
@login_required
def check_duplicate():
    """
    الفحص الفوري واللحظي للبيانات عبر السيرفر (الاسم، الجوال) أثناء الكتابة
    لمنع التكرار الرقمي وتأمين الحوكمة قبل الحفظ الكلي.
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()
    
    if not check_type or not value:
        return jsonify({"exists": False, "error": "Missing parameters"}), 400
        
    exists = False
    try:
        # 💡 استعلام الفحص الفوري من قاعدة البيانات لمنع التكرار:
        # if check_type == 'username':
        #     exists = Supplier.query.filter_by(username=value).first() is not None
        # elif check_type == 'owner_phone':
        #     exists = Supplier.query.filter_by(owner_phone=value).first() is not None
        pass
    except Exception as e:
        current_app.logger.error(f"❌ خطأ في فحص التكرار اللحظي: {str(e)}")
        
    return jsonify({"exists": exists})
