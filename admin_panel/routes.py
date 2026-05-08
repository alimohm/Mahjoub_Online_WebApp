import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_
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
    """ تأمين الـ APIs لمنع الدخول غير المصرح به """
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

# --- 3. مركز القيادة الإحصائي (Dashboard) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    
    try:
        users_count = User.query.count() if User else 1
        suppliers_count = Supplier.query.count() if Supplier else 0
        
        stats = {
            'suppliers_count': suppliers_count,
            'users_count': users_count,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        try:
            from core.models.business import Order
            stats['orders_count'] = Order.query.count()
        except:
            stats['orders_count'] = 0

        return render_template('dashboard.html', **stats)
    except Exception as e:
        return render_template('dashboard.html', users_count=1, suppliers_count=0, orders_count=0, now="إيقاع النظام مستقر")

# --- 4. إدارة الموردين (عرض الصفحة الرئيسية) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 5. محرك البحث السيادي (الـ API المخصص للترسانة) ---
@admin_bp.route('/api/suppliers/search')
@admin_api_required
def api_suppliers_search():
    """ محرك البحث الديناميكي الذي يغذي واجهة الترسانة """
    query_str = request.args.get('q', '').strip()
    province = request.args.get('province', '')
    district = request.args.get('district', '')
    tier = request.args.get('tier', '')
    status = request.args.get('status', '')

    # بناء الاستعلام الأساسي
    query = Supplier.query

    # إذا تم إدخال #، جلب الكل دون التقيد بنص البحث
    if query_str and query_str != '#':
        search_filter = or_(
            Supplier.owner_name.contains(query_str),
            Supplier.trade_name.contains(query_str),
            Supplier.username.contains(query_str),
            Supplier.phone.contains(query_str)
        )
        query = query.filter(search_filter)

    # تطبيق الفلاتر الإضافية
    if province: query = query.filter(Supplier.province == province)
    if district: query = query.filter(Supplier.district == district)
    if tier: query = query.filter(Supplier.tier == tier)
    if status: query = query.filter(Supplier.status == status)

    suppliers = query.order_by(Supplier.id.desc()).all()
    
    results = []
    for s in suppliers:
        results.append({
            "id": s.id,
            "owner_name": s.owner_name,
            "trade_name": s.trade_name,
            "username": s.username,
            "province": s.province,
            "district": s.district,
            "tier": getattr(s, 'tier', 'مبتدئ'),
            "balance_yer": float(getattr(s, 'balance_yer', 0)),
            "balance_sar": float(getattr(s, 'balance_sar', 0)),
            "balance_usd": float(getattr(s, 'balance_usd', 0)),
            "status": s.status
        })
    
    return jsonify(results)

# --- 6. جلب تفاصيل مورد واحد (للمودال) ---
@admin_bp.route('/api/suppliers/<int:sup_id>')
@admin_api_required
def api_get_supplier(sup_id):
    s = Supplier.query.get_or_404(sup_id)
    
    # جلب الموظفين إذا كان الموديل يدعم العلاقة
    staff_data = []
    if hasattr(s, 'staff_members'):
        for member in s.staff_members:
            staff_data.append({"id": member.id, "name": member.name, "role": member.role})

    return jsonify({
        "id": s.id,
        "owner_name": s.owner_name,
        "trade_name": s.trade_name,
        "username": s.username,
        "province": s.province,
        "district": s.district,
        "tier": getattr(s, 'tier', 'مبتدئ'),
        "balance_yer": float(getattr(s, 'balance_yer', 0)),
        "balance_sar": float(getattr(s, 'balance_sar', 0)),
        "balance_usd": float(getattr(s, 'balance_usd', 0)),
        "status": s.status,
        "staff": staff_data
    })

# --- 7. تعميد مورد جديد ---
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
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                status='active'
            )
            new_supplier.set_password(request.form.get('password', '123456'))
            
            db.session.add(new_supplier)
            db.session.flush() 
            
            if hasattr(new_supplier, 'mint_sovereign_id'):
                new_supplier.mint_sovereign_id()
                
            db.session.commit()
            
            if is_ajax: 
                return jsonify({'status': 'success', 'message': 'تم التعميد بنجاح'})
            flash("تم إضافة المورد الجديد للترسانة بنجاح", "success")
            return redirect(url_for('admin.manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax: return jsonify({'status': 'error', 'message': str(e)}), 400
            flash(f"عطل في بروتوكول الإضافة: {str(e)}", "danger")

    return render_template('add_supplier.html')

# --- 8. التحكم في الحالة وكلمة المرور ---
@admin_bp.route('/api/update-supplier-password/<int:sup_id>', methods=['POST'])
@admin_api_required
def update_supplier_password(sup_id):
    supplier = Supplier.query.get_or_404(sup_id)
    data = request.get_json()
    new_pass = data.get('password')
    
    if new_pass and len(new_pass) >= 6:
        supplier.set_password(new_pass)
        db.session.commit()
        return jsonify({"status": "success", "message": "تم تحديث كلمة المرور بنجاح"})
    return jsonify({"status": "error", "message": "كلمة المرور قصيرة جداً"}), 400

@admin_bp.route('/api/toggle-supplier-status/<int:sup_id>', methods=['POST'])
@admin_api_required
def toggle_supplier_status(sup_id):
    supplier = Supplier.query.get_or_404(sup_id)
    # تبديل الحالة تلقائياً
    supplier.status = 'suspended' if supplier.status == 'active' else 'active'
    db.session.commit()
    return jsonify({"status": "success", "new_status": supplier.status})

# --- 9. إنهاء الجلسة ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة السيادية بنجاح.", "info")
    return redirect(url_for('admin.login'))
