import os
import uuid
from flask import Blueprint, request, jsonify, render_template, current_app
from werkzeug.utils import secure_filename
from extensions import db  # أو كائن الـ db الخاص بمشروعك
from models import Supplier, Wallet  # استيراد النماذج الخاصة بقاعدة البيانات

# تعريف البلوبرنت الخاص بالموردين
suppliers_bp = Blueprint('suppliers', __name__, url_prefix='/admin/suppliers')

# الامتدادات المسموح بها لصور الوثائق
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_next_sequence():
    """
    توليد التسلسل التالي للمورد بناءً على آخر معرف مسجل في قاعدة البيانات
    التنسيق المتوقع: SUP-MAH9631 وما يليه
    """
    try:
        last_supplier = Supplier.query.filter(Supplier.sovereign_id.like('SUP-MAH%')).order_decay(Supplier.id.desc()).first()
        if last_supplier and last_supplier.sovereign_id:
            # استخراج الرقم من المعرف الحالي وزيادته بمقدار 1
            current_num = int(last_supplier.sovereign_id.split('SUP-MAH')[-1])
            next_num = current_num + 1
        else:
            next_num = 9631  # الرقم الابتدائي للتسلسل السيادي المعتمد
        return f"SUP-MAH{next_num}"
    except Exception as e:
        current_app.logger.error(f"Error generating sequence: {str(e)}")
        return "SUP-MAH9631"

@suppliers_bp.route('/check-duplicate', methods=['GET'])
def check_duplicate():
    """
    نقطة فحص التكرار وجلب التسلسل المتوقع عبر الـ Ajax ديباونس
    """
    check_type = request.args.get('type')
    value = request.args.get('value', '').strip()

    if check_type == 'get_next_sequence':
        next_seq = generate_next_sequence()
        return jsonify({'next_sequence': next_seq})

    if not check_type or not value:
        return jsonify({'exists': False}), 400

    exists = False
    if check_type == 'username':
        exists = db.session.query(Supplier.query.filter_by(username=value).exists()).scalar()
    elif check_type == 'identity_number':
        exists = db.session.query(Supplier.query.filter_by(identity_number=value).exists()).scalar()
    elif check_type == 'owner_name':
        exists = db.session.query(Supplier.query.filter_by(owner_name=value).exists()).scalar()
    elif check_type == 'trade_name':
        exists = db.session.query(Supplier.query.filter_by(trade_name=value).exists()).scalar()
    elif check_type == 'owner_phone':
        exists = db.session.query(Supplier.query.filter_by(owner_phone=value).exists()).scalar()
    elif check_type == 'bank_acc':
        exists = db.session.query(Supplier.query.filter_by(bank_acc=value).exists()).scalar()

    return jsonify({'exists': bool(exists)})

@suppliers_bp.route('/add', methods=['POST'])
def add_supplier():
    """
    استقبال البيانات، المعالجة، والتعميد النهائي في قاعدة البيانات
    """
    try:
        # استخراج البيانات الأساسية من الفورم
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')  # ينصح بتشفييرها باستخدام Werkzeug Security
        identity_type = request.form.get('identity_type', '')
        identity_number = request.form.get('identity_number', '').strip()
        owner_name = request.form.get('owner_name', '').strip()
        trade_name = request.form.get('trade_name', '').strip()
        owner_phone = request.form.get('owner_phone', '').strip()
        shop_phone = request.form.get('shop_phone', '').strip()
        province = request.form.get('province', '')
        district = request.form.get('district', '')
        address_detail = request.form.get('address_detail', '').strip()
        fin_type = request.form.get('fin_type', 'banks')
        bank_name = request.form.get('bank_name', '')
        bank_acc = request.form.get('bank_acc', '').strip()
        activity_type = request.form.get('activity_type', '')

        # التحقق من الحقول المطلوبة لضمان سلامة البيانات (Server-side validation)
        required_fields = [username, password, identity_type, identity_number, owner_name, trade_name, owner_phone, province, district, address_detail, bank_name, bank_acc]
        if any(not field for field in required_fields):
            return jsonify({'status': 'error', 'message': 'جميع الحقول الأساسية مطلوبة للتعميد السيادي.'}), 400

        # توليد المعرفات النهائية بشكل صارم لمنع التلاعب من الواجهة الأمامية
        sovereign_id = generate_next_sequence()
        wallet_code = sovereign_id.replace("SUP-", "WEL-", 1)

        # معالجة رفع الملف (صورة الوثيقة الثبوتية)
        identity_image_path = None
        if 'identity_image' in request.files:
            file = request.files['identity_image']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = f"{sovereign_id}_{secure_filename(file.filename)}"
                upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'suppliers')
                os.makedirs(upload_folder, exist_ok=True)
                file.save(os.path.join(upload_folder, filename))
                identity_image_path = f"uploads/suppliers/{filename}"

        # التحقق المزدوج من عدم التكرار في السيرفر قبل الإدخال (Race Condition Protection)
        duplicate_check = Supplier.query.filter(
            (Supplier.username == username) | 
            (Supplier.identity_number == identity_number) |
            (Supplier.owner_phone == owner_phone)
        ).first()
        
        if duplicate_check:
            return jsonify({'status': 'error', 'message': 'بيانات التوثيق أو اسم المستخدم مسجلة مسبقاً في النظام!'}), 400

        # إنشاء سجل المورد الجديد
        new_supplier = Supplier(
            sovereign_id=sovereign_id,
            username=username,
            password=password,  # يفضل عمل generate_password_hash(password) لحماية تامة
            identity_type=identity_type,
            identity_number=identity_number,
            identity_image=identity_image_path,
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
            status='active'
        )

        db.session.add(new_supplier)
        db.session.flush() # الحصول على المعرف الخاص بالمورد لربط المحفظة بشكل صحيح

        # إنشاء المحفظة الرقمية التابعة للمورد تلقائياً
        new_wallet = Wallet(
            supplier_id=new_supplier.id,
            wallet_code=wallet_code,
            balance=0.00,
            currency='YER'  # أو الفئة المالية المعتمدة في الإعدادات السيادية للمنصة
        )
        
        db.session.add(new_wallet)
        db.session.commit() # الحفظ النهائي لجميع الحقول والعمليات المتسلسلة

        # إرجاع رد النجاح متبوعاً بالبيانات لملء المودال التفاعلي
        return jsonify({
            'status': 'success',
            'message': 'تم تعميد المورد وإنشاء المحفظة المرتبطة بنجاح.',
            'redirect_url': '/admin/suppliers',
            'data': {
                'sovereign_id': sovereign_id,
                'wallet_code': wallet_code
            }
        }), 200

    except Exception as e:
        db.session.rollback() # التراجع فوراً عند حدوث أي خلل لحماية سلامة البيانات
        current_app.logger.error(f"Sovereign Archiving Failed: {str(e)}")
        return jsonify({'status': 'error', 'message': f'فشل داخلي في السيرفر السحابي: {str(e)}'}), 500
