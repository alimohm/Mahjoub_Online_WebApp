import os
from flask import render_template, request, redirect, url_for, flash, session, current_app
from flask_login import login_required, logout_user
from werkzeug.utils import secure_filename
from core import db 

# استيراد النماذج (Models) بمساراتها الصحيحة
try:
    from core.models import Vendor, User
    from core.models.vendor import WithdrawRequest
except ImportError:
    WithdrawRequest = None
    Vendor = None
    User = None

from . import admin_bp
from .auth import handle_admin_login

# إعداد مسار رفع الصور (تأكد من وجود المجلد static/uploads/ids)
UPLOAD_FOLDER = 'static/uploads/ids'

@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """إضافة مورد جديد لشبكة محجوب أونلاين مع أرشفة وثائق الهوية"""
    
    # حساب الرقم القادم تلقائياً للعرض في القالب
    next_id = 1001 # قيمة افتراضية
    if Vendor:
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        if last_vendor:
            next_id = last_vendor.id + 1

    if request.method == 'POST':
        # 1. استخراج البيانات من النموذج
        username = request.form.get('username')
        password = request.form.get('password')
        owner_name = request.form.get('owner_name')
        trade_name = request.form.get('trade_name')
        phone = request.form.get('phone')
        
        # 2. معالجة رفع صورة الهوية
        id_image = request.files.get('id_image')
        id_image_path = None
        
        if id_image and id_image.filename != '':
            filename = secure_filename(f"id_{username}_{id_image.filename}")
            # التأكد من وجود المجلد
            target_dir = os.path.join(current_app.root_path, UPLOAD_FOLDER)
            if not os.path.exists(target_dir):
                os.makedirs(target_dir)
            
            id_image.save(os.path.join(target_dir, filename))
            id_image_path = f"{UPLOAD_FOLDER}/{filename}"

        try:
            # 3. إنشاء حساب مستخدم (User) للمورد أولاً
            # ملاحظة: يتم تشفير كلمة المرور عادةً في الموديل أو باستخدام generate_password_hash
            new_user = User(username=username, role='vendor')
            new_user.set_password(password) # افترضنا وجود هذه الدالة في موديل User
            db.session.add(new_user)
            db.session.flush() # للحصول على user_id قبل الحفظ النهائي

            # 4. إنشاء سجل المورد (Vendor) وربطه بالمستخدم
            sovereign_id = str(next_id) # استخدام الـ ID كـ رقم محفظة سيادي موحد
            
            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=owner_name,
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                id_image_path=id_image_path,
                trade_name=trade_name,
                activity_type=request.form.get('activity_type'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                address_detail=request.form.get('address_detail'),
                phone=phone,
                e_wallet=sovereign_id, # الرقم الموحد
                fin_type=request.form.get('fin_type'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc')
            )
            
            db.session.add(new_vendor)
            db.session.commit()
            
            flash(f"تم تعميد المورد ({trade_name}) بنجاح. الرقم السيادي: {sovereign_id}", "success")
            return redirect(url_for('admin.admin_dashboard'))

        except Exception as e:
            db.session.rollback()
            flash(f"فشل نظام التعميد: {str(e)}", "danger")

    return render_template('add_supplier.html', next_id=next_id)

# ... باقي الدوال (login, logout, dashboard) تبقى كما هي ...
