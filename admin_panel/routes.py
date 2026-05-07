import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_, cast, String
from datetime import datetime
from functools import wraps

# الاستيراد من الهيكلية المعتمدة لترسانة محجوب أونلاين
from core.extensions import db 
from core.models.supplier import Supplier
from core.models.user import User

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي ---
def is_admin_sovereign():
    """ يضمن أن المؤسس علي محجوب فقط يمكنه الوصول. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

def admin_api_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not is_admin_sovereign():
            return jsonify({"status": "error", "message": "Access Denied: Sovereign Auth Required"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- 2. بوابة الدخول ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 3. مركز القيادة (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    try:
        stats = {
            'suppliers_count': Supplier.query.count(),
            'users_count': User.query.count(),
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return render_template('dashboard.html', **stats)
    except Exception as e:
        return render_template('dashboard.html', suppliers_count=0, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- 4. إدارة الموردين (تم تغيير الاسم لمنع التضارب) ---
@admin_bp.route('/manage-suppliers')
@login_required
def admin_manage_suppliers(): # تغيير الاسم من manage_suppliers لمنع AssertionError
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    all_suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
    return render_template('manage_suppliers.html', suppliers=all_suppliers)

# --- 5. بروتوكولات الـ API السيادية ---

@admin_bp.route('/api/supplier-details/<int:sup_id>')
@admin_api_required
def api_supplier_details(sup_id):
    supplier = Supplier.query.get_or_404(sup_id)
    return jsonify(supplier.to_dict())

@admin_bp.route('/api/toggle-supplier-status/<int:sup_id>', methods=['POST'])
@admin_api_required
def toggle_supplier_status(sup_id):
    supplier = Supplier.query.get_or_404(sup_id)
    data = request.get_json()
    new_status = data.get('status')
    
    if new_status in ['active', 'suspended']:
        supplier.status = new_status
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تحديث حالة المورد إلى {new_status}"})
    return jsonify({"status": "error", "message": "حالة غير صالحة"}), 400

# --- 6. تعميد مورد جديد ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            new_supplier = Supplier(
                username=request.form.get('username'),
                password=request.form.get('password', '123456'),
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                status='active'
            )
            db.session.add(new_supplier)
            db.session.flush() 
            new_supplier.mint_sovereign_id()
            db.session.commit()
            
            if is_ajax: 
                return jsonify({'status': 'success', 'message': 'تم التعميد بنجاح'})
            return redirect(url_for('admin.admin_manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax: return jsonify({'status': 'error', 'message': str(e)}), 400
            flash(f"خطأ: {str(e)}", "danger")

    return render_template('add_supplier.html')

# --- 7. إنهاء الجلسة ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة السيادية", "info")
    return redirect(url_for('admin.login'))
