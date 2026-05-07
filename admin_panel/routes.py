import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_
from datetime import datetime
from functools import wraps
from werkzeug.security import generate_password_hash

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
        # إحصائيات سريعة للوحة القيادة
        stats = {
            'suppliers_count': Supplier.query.count(),
            'users_count': User.query.count(), # يشمل الأدمن والموظفين
            'staff_count': User.query.filter_by(role='vendor_staff').count(),
            'now': datetime.now().strftime("%H:%M:%S")
        }
        return render_template('dashboard.html', **stats)
    except Exception as e:
        return render_template('dashboard.html', suppliers_count=0, now=datetime.now().strftime("%H:%M:%S"))

# --- 4. إدارة الموردين (واجهة التحكم الرئيسية) ---
@admin_bp.route('/manage-suppliers')
@login_required
def admin_manage_suppliers():
    """ عرض واجهة الإدارة - البيانات لا تظهر إلا عند البحث أو استخدام # """
    if not is_admin_sovereign():
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 5. بروتوكولات الـ API السيادية (البحث، التعديل، الموظفين) ---

@admin_bp.route('/api/search-suppliers')
@admin_api_required
def api_search_suppliers():
    """ محرك البحث المطور: يدعم اليوزرنيت ورمز (#) """
    q = request.args.get('q', '').strip()
    province = request.args.get('province', '').strip()
    tier = request.args.get('tier', '').strip()
    status = request.args.get('status', '').strip()

    if not q and not province and not tier and not status:
        return jsonify({"status": "success", "suppliers": []})

    query_obj = Supplier.query
    
    # بروتوكول الرمز (#) لاستدعاء الجميع
    if q == "#":
        pass 
    elif q:
        query_obj = query_obj.filter(
            or_(
                Supplier.username.ilike(f"%{q}%"),
                Supplier.trade_name.ilike(f"%{q}%"),
                Supplier.owner_name.ilike(f"%{q}%"),
                Supplier.phone.ilike(f"%{q}%")
            )
        )

    if province: query_obj = query_obj.filter_by(province=province)
    if tier: query_obj = query_obj.filter_by(tier=tier)
    if status: query_obj = query_obj.filter_by(status=status)

    suppliers = query_obj.order_by(Supplier.id.desc()).all()
    return jsonify({"status": "success", "suppliers": [s.to_dict() for s in suppliers]})

@admin_bp.route('/api/get-supplier-full-details/<int:s_id>')
@admin_api_required
def api_get_full_details(s_id):
    """ جلب بيانات المورد الكاملة مع طاقم موظفيه """
    supplier = Supplier.query.get_or_404(s_id)
    # جلب الموظفين المرتبطين بهذا المورد عبر اليوزرنيت (أو معرف الربط)
    staff = User.query.filter_by(role='vendor_staff').filter(User.username.like(f"{supplier.username}_%")).all()
    
    data = supplier.to_dict()
    data['staff'] = [{"id": u.id, "username": u.username} for u in staff]
    return jsonify(data)

@admin_bp.route('/api/update-sovereign-data/<int:s_id>', methods=['POST'])
@admin_api_required
def api_update_supplier(s_id):
    """ تعميد تحديث البيانات، الأرصدة الثلاثة، وكلمة المرور اليدوية """
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()

    try:
        supplier.owner_name = data.get('owner_name', supplier.owner_name)
        supplier.province = data.get('province', supplier.province)
        supplier.district = data.get('district', supplier.district)
        supplier.tier = data.get('tier', supplier.tier)
        
        # تحديث الخزينة الثلاثية
        supplier.balance_yer = data.get('balance_yer', supplier.balance_yer)
        supplier.balance_sar = data.get('balance_sar', supplier.balance_sar)
        supplier.balance_usd = data.get('balance_usd', supplier.balance_usd)

        # إعادة تعيين كلمة المرور يدوياً
        new_pass = data.get('new_password')
        if new_pass:
            supplier.password = generate_password_hash(new_pass)

        db.session.commit()
        return jsonify({"status": "success", "message": "تم تعميد التعديلات في الترسانة"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

@admin_bp.route('/api/add-supplier-staff/<int:s_id>', methods=['POST'])
@admin_api_required
def api_add_staff(s_id):
    """ إضافة موظف جديد للمورد بصلاحيات محددة (لا حذف ولا سحب) """
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "اسم المستخدم محجوز مسبقاً"}), 400

    new_staff = User(username=username, role='vendor_staff', is_active_account=True)
    new_staff.set_password(password)
    
    db.session.add(new_staff)
    db.session.commit()
    return jsonify({"status": "success", "message": f"تم تعيين الموظف {username} بنجاح"})

# --- 6. إنهاء الجلسة الآمنة ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة السيادية بنجاح", "info")
    return redirect(url_for('admin.login'))
