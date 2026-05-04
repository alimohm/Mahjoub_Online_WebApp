import os
import re
import random
import string
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 

# --- استيراد النماذج ---
try:
    from core.models.user import User
    from core.models.vendor import Vendor
    # استيراد النماذج الجديدة من ملف business
    from core.models.business import Province, District, FinancialEntity, Supplier, Order
except ImportError:
    User = Vendor = Province = District = FinancialEntity = Supplier = Order = None

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

# --- الربط مع الخدمات ---
try:
    from services.wallet_service import generate_wallet_id
except ImportError:
    def generate_wallet_id(next_id=None):
        if next_id:
            return f"W-{next_id}"
        return f"W-MAH-{random.randint(9000, 9999)}"

from . import admin_bp
from .auth import handle_admin_login

def get_next_sovereign_id():
    try:
        db.session.rollback()
        count = db.session.query(Vendor).count() if Vendor else 0
        return f"MAH-963{count + 1}"
    except:
        return f"MAH-963{random.randint(1, 99)}"

# --- 1. مسار الطوارئ، الترميم، والتعميد (المطور) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    try:
        db.session.rollback() 
        # 1. ترميم المستخدمين
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
        
        # 2. إنشاء الجداول الجديدة (التعميد السيادي)
        db.create_all()

        # 3. تغذية البيانات الجغرافية إذا كانت فارغة
        if Province and not Province.query.first():
            hodeidah = Province(name='الحديدة')
            aden = Province(name='عدن')
            db.session.add_all([hodeidah, aden])
            db.session.commit()
            
            # إضافة مديريات أساسية
            districts = [
                District(name='الخوخة', province_id=hodeidah.id),
                District(name='حيس', province_id=hodeidah.id),
                District(name='الشيخ عثمان', province_id=aden.id)
            ]
            db.session.add_all(districts)

        db.session.commit()
        session['repair_done'] = True
        flash("تم ترميم النظام وتعميد الجداول الجغرافية بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Error during repair: {str(e)}"

# --- 2. لوحة التحكم ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    try:
        db.session.rollback()
        stats = {'suppliers_count': 0, 'pending_withdrawals': 0, 'orders_count': 0}
        show_repair = not session.get('repair_done', False)

        if Vendor:
            stats['suppliers_count'] = db.session.query(Vendor).count()
        if WithdrawRequest:
            stats['pending_withdrawals'] = db.session.query(WithdrawRequest).filter_by(status='pending').count()
        
        return render_template('dashboard.html', **stats, show_repair=show_repair)
    except Exception as e:
        db.session.rollback()
        return render_template('dashboard.html', suppliers_count=0, pending_withdrawals=0, show_repair=True)

# --- 3. حوكمة الموردين (المسار المطور) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if request.method == 'POST':
        try:
            db.session.rollback()
            username = request.form.get('username')
            password = request.form.get('password')
            received_id = request.form.get('next_id') or get_next_sovereign_id()
            received_wallet = request.form.get('e_wallet') or generate_wallet_id(received_id)

            if User.query.filter_by(username=username).first():
                return jsonify({"status": "error", "message": "اسم المستخدم موجود مسبقاً"})

            new_user = User(username=username, role='vendor')
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.flush() 

            new_vendor = Vendor(
                user_id=new_user.id, 
                vendor_uid=received_id,
                owner_name=request.form.get('owner_name'), 
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'), 
                e_wallet=received_wallet,
                balance_yer=0.0, balance_sar=0.0, balance_usd=0.0,
                # تخزين الأسماء المختارة من القوائم
                province=request.form.get('province_name'), 
                district=request.form.get('district_name')
            )
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم تسجيل المورد في الترسانة بنجاح"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    # في حالة GET: جلب البيانات للقوائم المنسدلة
    provinces = Province.query.all() if Province else []
    banks = FinancialEntity.query.all() if FinancialEntity else []
    
    return render_template('add_supplier.html', 
                           provinces=provinces, 
                           banks=banks,
                           next_id=get_next_sovereign_id())

# مسار API لجلب المديريات للمتصفح
@admin_bp.route('/api/get-districts/<int:province_id>')
@login_required
def get_districts(province_id):
    districts = District.query.filter_by(province_id=province_id).all()
    return jsonify([{'id': d.id, 'name': d.name} for d in districts])

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    suppliers_list = Vendor.query.all() if Vendor else []
    return render_template('manage_suppliers.html', suppliers=suppliers_list)

# --- بقية المسارات (تسجيل الخروج والدخول) تبقى كما هي ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated and getattr(current_user, 'role', 'admin') == 'admin':
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    session.clear()
    flash('تم الخروج الآمن.', 'info')
    return redirect(url_for('admin.login'))
