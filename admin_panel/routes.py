import os
from flask import render_template, request, redirect, url_for, flash, session, current_app, jsonify
from flask_login import login_required, logout_user, current_user
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from core import db 

# --- استيراد النماذج (Models) مع معالجة الأخطاء لضمان تشغيل السيرفر ---
try:
    from core.models.vendor import Vendor
    from core.models.user import User  
    from core.models.vendor import WithdrawRequest 
except ImportError:
    Vendor = None
    User = None
    WithdrawRequest = None

# --- استيراد مدير الأرشفة السيادي (GitHub Archive) ---
# ملاحظة: إذا فشل استيراد الأرشيف، سيعمل النظام محلياً فقط ولن ينهار
try:
    from .archive_manager import ArchiveManager
    archiver = ArchiveManager()
except (ImportError, Exception):
    archiver = None

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بوابة الدخول والخروج ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """بوابة الدخول إلى النظام السيادي"""
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
    """عرض إحصائيات منصة محجوب أونلاين"""
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
    إدارة عملية التعميد السيادي الكاملة
    """
    # توليد المعرف السيادي التالي
    next_id = 1001
    try:
        if Vendor:
            last_vendor = Vendor.query.order_by(Vendor.id.desc()).first()
            if last_vendor:
                next_id = last_vendor.id + 1
    except Exception:
        next_id = "Auto"

    if request.method == 'POST':
        try:
            # أ- استلام البيانات من النموذج الملكي
            username = request.form.get('username')
            password = request.form.get('password', '123')
            e_wallet = request.form.get('e_wallet')
            
            activity = request.form.get('manual_activity') if request.form.get('activity_type') == 'manual' else request.form.get('activity_type')
            
            # ب- الأرشفة السيادية (GitHub) - تعمل فقط إذا كان الموديل متاحاً
            github_path = "Local_Only"
            id_file = request.files.get('id_image')
            
            if archiver and id_file and id_file.filename:
                ext = os.path.splitext(id_file.filename)[1]
                file_data = id_file.read()
                
                github_path = archiver.upload_document(
                    s_id=e_wallet, 
                    u_id=username, 
                    doc_t="Identity_Doc", 
                    file_d=file_data, 
                    ext=ext
                )
                
                archiver.upload_full_package(
                    data={
                        'sovereign_id': e_wallet,
                        'owner_name': request.form.get('owner_name'),
                        'trade_name': request.form.get('trade_name'),
                        'status': 'Verified_By_Ali_Mahjoub'
                    },
                    files=[]
                )

            # ج- الحفظ في قاعدة البيانات المحلية
            new_user = User(
                username=username,
                password=generate_password_hash(password),
                role='vendor'
            )
            db.session.add(new_user)
            db.session.flush()

            new_vendor = Vendor(
                user_id=new_user.id,
                owner_name=request.form.get('owner_name'),
                id_card_number=request.form.get('id_card_number'),
                id_image_path=github_path,
                trade_name=request.form.get('trade_name'),
                activity_type=activity,
                province=request.form.get('province'),
                district=request.form.get('district'),
                e_wallet=e_wallet,
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                is_verified=True
            )
            
            db.session.add(new_vendor)
            db.session.commit()

            return jsonify({"status": "success", "message": "تم التعميد والأرشفة بنجاح"}), 200

        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": f"خطأ في البيانات: {str(e)}"}), 500

    return render_template('add_supplier.html', next_id=next_id)

# --- 4. طلبات السحب والمحافظ ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    requests_list = WithdrawRequest.query.filter_by(status='pending').all() if WithdrawRequest else []
    return render_template('withdraw_requests.html', requests=requests_list)

@admin_bp.route('/wallets')
@login_required
def wallets():
    all_vendors = Vendor.query.all() if Vendor else []
    return render_template('wallets.html', vendors=all_vendors)
