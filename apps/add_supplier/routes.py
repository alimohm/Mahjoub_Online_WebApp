import os
import uuid
from flask import Blueprint, request, jsonify, render_template, current_app
from werkzeug.utils import secure_filename
from extensions import db  # أو كائن الـ db الخاص بمشروعك
from models import Supplier, Wallet  # استيراد النماذج الخاصة بقاعدة البيانات

# # coding: utf-8
import os
import secrets
from flask import Blueprint, render_template, request, jsonify, current_app, url_for
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash

from apps import db
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import Wallet

admin_suppliers_bp = Blueprint(
    'admin_suppliers', 
    __name__, 
    template_folder='templates',
    static_folder='static'
)

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'pdf'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ─── المسارات (Routes) ───

@admin_suppliers_bp.route('/admin/suppliers/add', methods=['GET', 'POST'])
def add_supplier_page():
    """
    عرض صفحة تعميد المورد والمعالجة السحابية الفورية والسريعة بدون تعليق.
    """
    if request.method == 'POST':
        try:
            # استقبال البيانات الأساسية وتنظيفها
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

            # التحقق الخلفي من الحقول الإلزامية
            if not all([username, password, identity_type, identity_number, owner_name, trade_name, owner_phone, province, district, address_detail, bank_name, bank_acc]):
                return jsonify({"status": "error", "message": "⚠️ جميع الحقول الإلزامية يجب أن تكون مكتملة وصحيحة."}), 400

            # فحص ومنع تكرار البيانات الحيوية
            if Supplier.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم هذا محجوز مسبقاً."}), 400
            if Supplier.query.filter_by(identity_number=identity_number).first():
                return jsonify({"status": "error", "message": "رقم الوثيقة / الهوية مسجل مسبقاً."}), 400

            # معالجة رفع الملفات
            identity_image_db_path = None
            if 'identity_image' in request.files:
                file = request.files['identity_image']
                if file and file.filename != '' and allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    unique_filename = f"doc_{secrets.token_hex(8)}_{filename}"
                    base_upload_folder = os.path.join(current_app.root_path, 'static', 'uploads', 'identities')
                    os.makedirs(base_upload_folder, exist_ok=True)
                    file.save(os.path.join(base_upload_folder, unique_filename))
                    identity_image_db_path = f"uploads/identities/{unique_filename}"

            # توليد الهويات السيادية الرقمية المعتمدة في الموديل الخاص بك
            generated_sovereign_id = Supplier.generate_next_sovereign_id()
            
            if generated_sovereign_id.startswith("SUP-"):
                generated_wallet_code = generated_sovereign_id.replace("SUP-", "WEL-", 1)
            else:
                generated_wallet_code = f"WEL-{generated_sovereign_id}"

            hashed_password = generate_password_hash(password)

            # تأسيس كائن المورد
            new_supplier = Supplier(
                username=username,
                password_hash=hashed_password,  
                sovereign_id=generated_sovereign_id,
                wallet_code=generated_wallet_code,
                identity_type=identity_type,
                identity_number=identity_number,
                identity_image=identity_image_db_path,
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
                status="نشط"
            )
            db.session.add(new_supplier)
            
            # حجز الهوية في الجلسة أولاً لتوفير معرف الـ ID الفعلي وتفادي قيود المفاتيح الأجنبية
            db.session.flush()

            # تأسيس كائن المحفظة النقي والمستقر بالأرصدة التأسيسية المتعددة (ريال يمني، سعودي، دولار)
            new_wallet = Wallet(
                wallet_code=generated_wallet_code,
                # ملاحظة أمان: نستخدم معرف الـ id الراجع بعد الـ flush للتأكد من ربط العلاقات بشكل سليم ومطلق بمفتاح الجدول الأساسي.
                supplier_id=new_supplier.id, 
                yer_total=0.0, yer_withdrawn=0.0, yer_pending=0.0,
                sar_total=0.0, sar_withdrawn=0.0, sar_pending=0.0,
                usd_total=0.0, usd_withdrawn=0.0, usd_pending=0.0,
                status="نشطة"
            )
            db.session.add(new_wallet)

            # التثبيت النهائي الشامل لكافة الجداول والعمليات المترابطة بقاعدة البيانات
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": "تم الحفظ الفعلي وتعميد المحفظة بنجاح مطلق.",
                "redirect_url": url_for('admin_dashboard.list_suppliers'),  
                "data": {
                    "sovereign_id": generated_sovereign_id,
                    "wallet_code": generated_wallet_code
                }
            }), 200

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"❌ خطأ تعميد المورد السحابي: {str(e)}")
            return jsonify({"status": "error", "message": f"فشل داخلي في السيرفر السحابي (500): {str(e)}"}), 500
        finally:
            db.session.close()  # 🔓 تحرير الاتصال فوراً وبشكل حازم لمنع تعليق قاعدة البيانات مستقبلاً

    # في حالة طلب GET، نمرر الإعدادات إلى صفحة HTML العامة
    endpoints_config = {
        "add_supplier": url_for('admin_suppliers.add_supplier_page'),
        "check_duplicate": url_for('admin_suppliers.check_duplicate')
    }
    return render_template('admin/add_supplier.html', endpoints=endpoints_config)


@admin_suppliers_bp.route('/admin/suppliers/check-duplicate', methods=['GET'])
def check_duplicate():
    check_type = request.args.get('type', '')
    value = request.args.get('value', '').strip()

    if not check_type or not value or check_type not in ['username', 'identity_number', 'owner_phone', 'trade_name', 'bank_acc']:
        return jsonify({"exists": False, "error": "المعاملات البرمجية غير مدعومة"}), 400

    try:
        exists = db.session.query(Supplier).filter(getattr(Supplier, check_type) == value).first() is not None
        return jsonify({"exists": bool(exists)})
    except Exception:
        return jsonify({"exists": False, "error": "فشل فحص قاعدة البيانات"})
    finally:
        db.session.close()  # 🔓 تحرير الاتصال فوراً لحفظ طاقة السيرفر البلوبرنت الخاص بالموردين
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
