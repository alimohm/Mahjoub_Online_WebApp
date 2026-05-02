import os
from flask import render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from core import db 

# استيراد النماذج (Models)
try:
    from core.models.vendor import Vendor
    from core.models.user import User  
    from core.models.vendor import WithdrawRequest 
except ImportError:
    Vendor = None
    User = None
    WithdrawRequest = None

# استيراد مدير الأرشفة السيادي (GitHub Archive)
from .archive_manager import ArchiveManager

from . import admin_bp
from .auth import handle_admin_login

# تهيئة مدير الأرشفة
archiver = ArchiveManager()

# --- 1. بوابة الدخول والخروج ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash("تم تأمين الخروج من النظام السيادي.", "info")
    return redirect(url_for('admin.login'))

# --- 2. لوحة التحكم الرئيسية ---
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    suppliers_count = Vendor.query.count() if Vendor else 0
    pending_withdrawals = WithdrawRequest.query.filter_by(status='pending').count() if WithdrawRequest else 0
    return render_template('dashboard.html', 
                           suppliers_count=suppliers_count, 
                           pending_withdrawals=pending_withdrawals)

# --- 3. إدارة الموردين (التعميد والأرشفة) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    """
    إدارة عملية التعميد السيادي:
    1. توليد الرقم التسلسلي (ID) ليكون هو نفسه رقم المحفظة.
    2. الأرشفة الضوئية للوثائق والبيانات في GitHub.
    3. إنشاء حساب المستخدم وملف المورد في قاعدة البيانات المحلية.
    """
    
    # منطق توليد الرقم السيادي (يبدأ من 1001)
    next_id = 1001
    if Vendor:
        last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
        if last_vendor:
            # زيادة بمقدار 1 لضمان التسلسل (مثل: 1001, 1002, 1003...)
            next_id = last_vendor.id + 1001 

    if request.method == 'POST':
        try:
            # أ- استلام البيانات من النموذج الملكي
            username = request.form.get('username')
            password = request.form.get('password', '123')
            # الأيدي القادم من الواجهة (المحفظة السيادية)
            e_wallet = request.form.get('e_wallet') 
            
            # معالجة المدخلات (اختيار من القائمة أو إدخال يدوي)
            activity = request.form.get('manual_activity') if request.form.get('activity_type') == 'manual' else request.form.get('activity_type')
            
            # ب- الأرشفة الخارجية الهرمية (GitHub)
            id_file = request.files.get('id_image')
            github_path = None
            
            if id_file and id_file.filename:
                ext = os.path.splitext(id_file.filename)[1]
                file_data = id_file.read()
                
                # 1. رفع صورة الهوية (أرشفة ضوئية سيادية)
                github_path = archiver.upload_document(
                    s_id=e_wallet, 
                    u_id=username, 
                    doc_t="Identity_Doc", 
                    file_d=file_data, 
                    ext=ext
                )
                
                # 2. أرشفة السجل النصي الكامل (JSON) لضمان عدم ضياع البيانات مستقبلاً
                archiver.upload_full_package(
                    data={
                        'sovereign_id': e_wallet,
                        'username': username,
                        'owner_name': request.form.get('owner_name'),
                        'trade_name': request.form.get('trade_name'),
                        'activity': activity,
                        'location': f"{request.form.get('province')} - {request.form.get('district')}",
                        'bank_info': f"{request.form.get('bank_name')} - {request.form.get('bank_acc')}",
                        'status': 'Verified_By_Ali_Mahjoub'
                    },
                    files=[] # تم رفع الوثائق بشكل منفصل
                )

            # ج- إنشاء السجلات في قاعدة البيانات (SQL)
            # 1. إنشاء حساب المستخدم (Authentication)
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                role='vendor'
            )
            db.session.add(new_user)
            db.session.flush() # الحصول على ID المستخدم قبل الحفظ النهائي

            # 2. إنشاء ملف المورد (Business Profile)
            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=request.form.get('owner_name'),
                id_card_number=request.form.get('id_card_number'),
                id_image_path=github_path, # تخزين رابط الأرشيف السيادي
                trade_name=request.form.get('trade_name'),
                activity_type=activity,
                province=request.form.get('province'),
                district=request.form.get('district'),
                e_wallet=e_wallet, # المحفظة الذكية
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                is_verified=True # تعميد فوري عند الإضافة من قبل المدير
            )
            
            db.session.add(new_vendor)
            db.session.commit()

            # إرسال استجابة نجاح (لتعمل مع SweetAlert2 في الواجهة)
            return jsonify({"status": "success", "message": "تم التعميد والأرشفة بنجاح"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"فشل التعميد: {str(e)}"}), 500

    return render_template('add_supplier.html', next_id=next_id)

# --- 4. طلبات السحب ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    requests_list = WithdrawRequest.query.filter_by(status='pending').all() if WithdrawRequest else []
    return render_template('withdraw_requests.html', requests=requests_list)

# --- 5. إدارة المحافظ السيادية ---
@admin_bp.route('/wallets')
@login_required
def wallets():
    all_vendors = Vendor.query.all() if Vendor else []
    return render_template('wallets.html', vendors=all_vendors)
