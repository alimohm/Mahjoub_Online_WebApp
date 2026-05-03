import os
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 

# استيراد النماذج بحذر شديد لضمان استقرار النظام
try:
    from core.models.user import User
    from core.models.vendor import Vendor
except ImportError:
    User = None
    Vendor = None

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

from . import admin_bp
from .auth import handle_admin_login

# --- 1. مسار الطوارئ السيادي (إصلاح شامل لقاعدة البيانات) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    db.session.rollback() # إنهاء أي ترانزاكشن معلق
    try:
        # تنفيذ أوامر الترميم المباشرة لإضافة الأعمدة الناقصة
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
        db.session.execute(text("ALTER TABLE vendors ADD COLUMN IF NOT EXISTS user_id INTEGER;"))
        
        db.session.commit()
        session['repair_done'] = True
        return """
        <div style="text-align:center; margin-top:50px; font-family:sans-serif; direction:rtl;">
            <h1 style="color: #632C8F;">✨ تم اكتمال الترميم الهيكلي بنجاح!</h1>
            <p style="color: #1a0b2e;">تم تحديث الجداول لتتوافق مع معايير محجوب أونلاين.</p>
            <a href="/admin/dashboard" style="padding:12px 25px; background:#632C8F; color:white; text-decoration:none; border-radius:10px;">دخول مركز القيادة (Dashboard)</a>
        </div>
        """
    except Exception as e:
        db.session.rollback()
        return f"<h1 style='color:red; text-align:center;'>❌ فشل الترميم: {str(e)}</h1>"

# --- 2. لوحة التحكم المركزية (الداشبورد) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    db.session.rollback()
    stats = {'suppliers_count': 0, 'pending_withdrawals': 0, 'orders_count': 0, 'total_balance': "0.00"}
    show_repair = not session.get('repair_done', False)

    try:
        if Vendor:
            stats['suppliers_count'] = db.session.query(Vendor).count()
        if WithdrawRequest:
            stats['pending_withdrawals'] = db.session.query(WithdrawRequest).filter_by(status='pending').count()
    except Exception as e:
        db.session.rollback()
        show_repair = True 
    
    return render_template('dashboard.html', **stats, show_repair=show_repair)

# --- 3. حوكمة الموردين وتعيدهم ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    db.session.rollback()
    
    if request.method == 'POST':
        try:
            # استخراج البيانات من النموذج (Form)
            username = request.form.get('username')
            password = request.form.get('password')
            trade_name = request.form.get('trade_name')
            owner_name = request.form.get('owner_name')
            phone = request.form.get('phone')
            wallet_id = request.form.get('e_wallet') # الرقم السيادي

            # 1. إنشاء حساب المستخدم (User) المرتبط بالمورد
            if User:
                new_user = User(
                    username=username,
                    role='vendor' # تحديد الصلاحية كمورد
                )
                new_user.set_password(password)
                db.session.add(new_user)
                db.session.flush() # الحصول على ID المستخدم قبل الحفظ النهائي

                # 2. إنشاء بيانات المورد (Vendor)
                if Vendor:
                    new_vendor = Vendor(
                        user_id=new_user.id,
                        store_name=trade_name,
                        owner_full_name=owner_name,
                        phone_number=phone,
                        wallet_number=wallet_id,
                        activity_type=request.form.get('activity_type')
                    )
                    db.session.add(new_vendor)
            
            db.session.commit()
            
            # الرد بصيغة JSON لنجاح عملية التعميد (لمنع خطأ الـ JavaScript)
            return jsonify({
                "status": "success",
                "message": "تم الأرشفة والتعميد السيادي بنجاح"
            })

        except Exception as e:
            db.session.rollback()
            return jsonify({
                "status": "error",
                "message": f"فشل التعميد: {str(e)}"
            }), 500

    # في حالة الـ GET: توليد الرقم السيادي التالي
    last_vendor = Vendor.query.order_by(Vendor.id.desc()).first() if Vendor else None
    next_id_num = (last_vendor.id + 1) if last_vendor else 1001
    next_id = f"MAH-{next_id_num}"

    return render_template('add_supplier.html', next_id=next_id)

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    db.session.rollback()
    suppliers_list = []
    try:
        suppliers_list = Vendor.query.all() if Vendor else []
    except:
        db.session.rollback()
    return render_template('manage_suppliers.html', suppliers=suppliers_list)

# --- 4. الهندسة المالية (طلبات السحب) ---
@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    db.session.rollback()
    requests_list = []
    if WithdrawRequest:
        try:
            requests_list = WithdrawRequest.query.order_by(WithdrawRequest.id.desc()).all()
        except:
            db.session.rollback()
    return render_template('withdraw_requests.html', requests=requests_list)

# --- 5. إدارة الجلسات السيادية ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    db.session.rollback()
    if current_user.is_authenticated:
        try:
            user_role = getattr(current_user, 'role', 'admin')
            if user_role == 'admin':
                return redirect(url_for('admin.admin_dashboard'))
        except:
            db.session.rollback()
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('تم إغلاق الجلسة الآمنة بنجاح.', 'info')
    return redirect(url_for('admin.login'))
