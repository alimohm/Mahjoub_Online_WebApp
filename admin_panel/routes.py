import os
import re
import random
import string
from flask import render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from sqlalchemy import text
from core import db 

# --- 1. استيراد النماذج مع حماية من أخطاء الاستيراد ---
try:
    from core.models.user import User
    from core.models.vendor import Vendor
    from core.models.business import Province, District, FinancialEntity, Supplier, Order
except ImportError:
    User = Vendor = Province = District = FinancialEntity = Supplier = Order = None

try:
    from core.models.vendor import WithdrawRequest 
except ImportError:
    WithdrawRequest = None

# --- 2. خدمات المحافظ والهوية ---
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
        return f"MAH-963{random.randint(100, 999)}"

# --- 3. مسار الطوارئ (الإصلاح الشامل) ---
@admin_bp.route('/force-repair-now')
def force_repair():
    try:
        db.session.rollback() 
        # تحديث هيكل الجداول
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS role VARCHAR(50) DEFAULT 'admin';"))
        db.session.execute(text("ALTER TABLE users ADD COLUMN IF NOT EXISTS is_active_account BOOLEAN DEFAULT TRUE;"))
        db.create_all()

        # تعميد البيانات الأساسية للمحافظات
        if Province and not Province.query.first():
            hodeidah = Province(name='الحديدة')
            aden = Province(name='عدن')
            db.session.add_all([hodeidah, aden])
            db.session.commit()
            
            districts = [
                District(name='الخوخة', province_id=hodeidah.id),
                District(name='حيس', province_id=hodeidah.id),
                District(name='الشيخ عثمان', province_id=aden.id)
            ]
            db.session.add_all(districts)

        db.session.commit()
        session['repair_done'] = True
        flash("تم تعميد النظام بنجاح", "success")
        return redirect(url_for('admin.admin_dashboard'))
    except Exception as e:
        db.session.rollback()
        return f"Repair Error: {str(e)}"

# --- 4. لوحة التحكم (Dashboard) ---
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

# --- 5. حوكمة الموردين (المسار الذي واجه الخطأ) ---
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
                user_id=new_user.id, vendor_uid=received_id,
                owner_name=request.form.get('owner_name'), trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'), e_wallet=received_wallet,
                balance_yer=0.0, balance_sar=0.0, balance_usd=0.0,
                province=request.form.get('province_name'), 
                district=request.form.get('district_name')
            )
            db.session.add(new_vendor)
            db.session.commit()
            return jsonify({"status": "success", "message": "تم تعميد المورد بنجاح"})
        except Exception as e:
            db.session.rollback()
            return jsonify({"status": "error", "message": str(e)}), 500

    # معالجة الـ GET لضمان عدم انهيار الصفحة
    try:
        provinces = Province.query.all() if Province else []
        banks = FinancialEntity.query.all() if FinancialEntity else []
    except:
        db.session.rollback()
        provinces, banks = [], []

    return render_template('add_supplier.html', 
                           provinces=provinces, 
                           banks=banks, 
                           next_id=get_next_sovereign_id())

@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    try:
        suppliers_list = Vendor.query.all() if Vendor else []
        return render_template('manage_suppliers.html', suppliers=suppliers_list)
    except:
        db.session.rollback()
        return render_template('manage_suppliers.html', suppliers=[])

# --- 6. المحافظ وطلبات السحب ---
@admin_bp.route('/manage-wallets')
@login_required
def manage_wallets():
    try:
        suppliers_list = Vendor.query.all() if Vendor else []
        return render_template('wallets.html', suppliers=suppliers_list)
    except:
        db.session.rollback()
        return render_template('wallets.html', suppliers=[])

@admin_bp.route('/withdraw-requests')
@login_required
def withdraw_requests():
    requests = WithdrawRequest.query.all() if WithdrawRequest else []
    return render_template('manage_suppliers.html', suppliers=[], withdraw_requests=requests)

# --- 7. خدمات الـ API والدخول ---
@admin_bp.route('/api/get-districts/<int:province_id>')
@login_required
def get_districts(province_id):
    try:
        districts = District.query.filter_by(province_id=province_id).all()
        return jsonify([{'id': d.id, 'name': d.name} for d in districts])
    except:
        return jsonify([])

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
    flash('تم تسجيل الخروج.', 'info')
    return redirect(url_for('admin.login'))
