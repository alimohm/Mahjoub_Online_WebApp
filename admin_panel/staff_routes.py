from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from core.models.user import User
from core.extensions import db
import json

staff_bp = Blueprint('staff', __name__, url_prefix='/admin/staff')

@staff_bp.route('/manage')
@login_required
def manage_staff():
    # جلب فريق الإدارة (الذين لا يتبعون مورد معين)
    admin_team = User.query.filter(User.supplier_id == None, User.role != 'super_admin').all()
    return render_template('staff/manage_staff.html', admin_team=admin_team)

@staff_bp.route('/add', methods=['POST'])
@login_required
def add_staff_member():
    if not current_user.role == 'super_admin':
        flash('صلاحية سيادية مطلوبة لهذا الإجراء!', 'danger')
        return redirect(url_for('staff.manage_staff'))

    username = request.form.get('username')
    password = request.form.get('password')
    full_name = request.form.get('full_name')
    role = request.form.get('role')
    
    # تجميع الصلاحيات المحددة من الواجهة
    perms = {
        "can_manage_suppliers": 'manage_suppliers' in request.form,
        "can_approve_products": 'approve_products' in request.form,
        "can_view_finance": 'view_finance' in request.form
    }

    if User.query.filter_by(username=username).first():
        flash('اسم المستخدم موجود مسبقاً في النظام!', 'warning')
        return redirect(url_for('staff.manage_staff'))

    new_member = User(
        username=username,
        full_name=full_name,
        role=role,
        permissions=json.dumps(perms)
    )
    new_member.set_password(password)
    
    db.session.add(new_member)
    db.session.commit()
    
    flash(f'تم تعميد الموظف {full_name} بنجاح في نظام الإدارة.', 'success')
    return redirect(url_for('staff.manage_staff'))
