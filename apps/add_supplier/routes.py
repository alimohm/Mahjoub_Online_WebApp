import os
from flask import Blueprint, render_template, request, jsonify, url_for, current_app
from werkzeug.utils import secure_filename
from datetime import datetime

# تعريف الـ Blueprint الخاص بالإدارة
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

# إعدادات الامتدادات المسموحة للصور
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'webp'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_bp.route('/suppliers/add', methods=['GET', 'POST'])
def add_supplier():
    if request.method == 'POST':
        try:
            # 1. استخراج البيانات الأساسية
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            activity_type = request.form.get('activity_type') # القيمة من الحقل المخفي

            # 2. بيانات التوثيق والمالك
            owner_name = request.form.get('owner_name')
            identity_type = request.form.get('identity_type')
            trade_name = request.form.get('trade_name')
            phone = request.form.get('phone')

            # 3. البيانات المالية والجغرافية
            bank_name = request.form.get('bank_name') # القيمة من الحقل المخفي
            bank_acc = request.form.get('bank_acc')
            province = request.form.get('province')
            district = request.form.get('district')
            address_detail = request.form.get('address_detail')

            # 4. معالجة رفع صورة الهوية
            identity_image_path = None
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and allowed_file(file.filename):
                    filename = f"ID_{username}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{file.filename.rsplit('.', 1)[1].lower()}"
                    filename = secure_filename(filename)
                    
                    # تأكد من إنشاء مجلد الرفع
                    upload_folder = os.path.join(current_app.root_path, 'static/uploads/suppliers/ids')
                    if not os.path.exists(upload_folder):
                        os.makedirs(upload_folder)
                    
                    file.save(os.path.join(upload_folder, filename))
                    identity_image_path = f"uploads/suppliers/ids/{filename}"

            # 5. منطق الحفظ في قاعدة البيانات (مثال توضيحي)
            # new_supplier = Supplier(
            #     username=username,
            #     owner_name=owner_name,
            #     trade_name=trade_name,
            #     activity_type=activity_type,
            #     phone=phone,
            #     bank_name=bank_name,
            #     bank_acc=bank_acc,
            #     province=province,
            #     district=district,
            #     identity_image=identity_image_path,
            #     status='active'
            # )
            # db.session.add(new_supplier)
            # db.session.commit()

            # إرجاع استجابة نجاح متوافقة مع AJAX في القالب
            return jsonify({
                "status": "success",
                "message": f"تم تعميد المورد '{trade_name}' بنجاح وأرشفته في النظام السيادي."
            })

        except Exception as e:
            return jsonify({
                "status": "error",
                "message": f"حدث خطأ أثناء الأرشفة: {str(e)}"
            }), 500

    # في حالة GET: عرض الصفحة
    # يمكنك حساب next_id من قاعدة البيانات
    next_id = 101 # مثال
    return render_template('admin/add_supplier.html', next_id=next_id)

@admin_bp.route('/dashboard')
def dashboard():
    return "لوحة التحكم"
