from flask import render_template, request, jsonify
from sqlalchemy import or_, cast, String
from core.models.supplier import Supplier
from core.models.user import User
from core.extensions import db
from . import admin_bp
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.security import generate_password_hash

# --- 1. بروتوكول الحماية السيادية ---
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            return jsonify({"status": "error", "message": "صلاحيات غير كافية"}), 403
        return f(*args, **kwargs)
    return decorated_function

# --- 2. المحرك الرئيسي للبحث والاستدعاء (The Recall Engine) ---
@admin_bp.route('/api/search-suppliers')
@login_required
@admin_required
def api_search_suppliers():
    """البحث الذكي: يدعم الاسم، اليوزرنيت، الهاتف، ورمز (#) للكل"""
    q = request.args.get('q', '').strip()
    province = request.args.get('province', '').strip()
    district = request.args.get('district', '').strip()
    tier = request.args.get('tier', '').strip()
    status = request.args.get('status', '').strip()

    # إذا لم يتم إدخال بحث ولا رمز #، نرجع قائمة فارغة (Zero-Load)
    if not q:
        return jsonify({"status": "success", "suppliers": [], "count": 0})

    query_obj = Supplier.query

    # منطق الرمز (#) لاستدعاء الجميع
    if q == "#":
        pass # استمر بدون فلتر نصي لجلب الكل
    else:
        # البحث في الموردين (اسم المستخدم، اسم المتجر، الهاتف)
        query_obj = query_obj.filter(
            or_(
                Supplier.username.ilike(f"%{q}%"),
                Supplier.trade_name.ilike(f"%{q}%"),
                Supplier.owner_name.ilike(f"%{q}%"),
                Supplier.phone.ilike(f"%{q}%"),
                Supplier.e_wallet.ilike(f"%{q}%")
            )
        )

    # تطبيق الفلاتر الإضافية
    if province: query_obj = query_obj.filter_by(province=province)
    if district: query_obj = query_obj.filter_by(district=district)
    if tier: query_obj = query_obj.filter_by(tier=tier)
    if status: query_obj = query_obj.filter_by(status=status)

    suppliers = query_obj.order_by(Supplier.id.desc()).all()
    
    return jsonify({
        "status": "success",
        "count": len(suppliers),
        "suppliers": [s.to_dict() for s in suppliers]
    })

# --- 3. جلب تفاصيل الكيان والموظفين (The Sync Point) ---
@admin_bp.route('/api/get-supplier-full-details/<int:s_id>')
@login_required
@admin_required
def get_supplier_full_details(s_id):
    supplier = Supplier.query.get_or_404(s_id)
    
    # جلب الموظفين المرتبطين بهذا المورد من جدول المستخدمين
    # ملاحظة: نفترض وجود حقل supplier_reference يربط الموظف بمورده
    staff_members = User.query.filter_by(role='vendor_staff', username=supplier.username).all()
    
    data = supplier.to_dict()
    data['staff'] = [{
        "id": user.id,
        "username": user.username,
        "is_active": user.is_active_account
    } for user in staff_members]
    
    return jsonify(data)

# --- 4. تعميد التعديلات السيادية (Update & Currency) ---
@admin_bp.route('/api/update-sovereign-data/<int:s_id>', methods=['POST'])
@login_required
@admin_required
def update_sovereign_data(s_id):
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()

    try:
        # 1. تحديث البيانات الأساسية
        supplier.owner_name = data.get('owner_name', supplier.owner_name)
        supplier.province = data.get('province', supplier.province)
        supplier.district = data.get('district', supplier.district)
        supplier.tier = data.get('tier', supplier.tier)
        
        # 2. تحديث الخزينة الثلاثية
        supplier.balance_yer = data.get('balance_yer', supplier.balance_yer)
        supplier.balance_sar = data.get('balance_sar', supplier.balance_sar)
        supplier.balance_usd = data.get('balance_usd', supplier.balance_usd)

        # 3. إعادة تعيين كلمة المرور يدوياً (إذا أُرسلت)
        new_pass = data.get('new_password')
        if new_pass and len(new_pass) >= 4:
            # تحديث كلمة المورد في جدول الموردين
            supplier.password = generate_password_hash(new_pass) 

        db.session.commit()
        return jsonify({"status": "success", "message": "تم تعميد كافة البيانات والأرصدة في القاعدة"})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 500

# --- 5. بوابة إضافة موظف جديد يدوياً (Staff Induction) ---
@admin_bp.route('/api/add-supplier-staff/<int:s_id>', methods=['POST'])
@login_required
@admin_required
def add_supplier_staff(s_id):
    supplier = Supplier.query.get_or_404(s_id)
    data = request.get_json()
    
    username = data.get('username')
    password = data.get('password')

    if User.query.filter_by(username=username).first():
        return jsonify({"status": "error", "message": "اسم المستخدم موجود مسبقاً"}), 400

    new_staff = User(
        username=username,
        role='vendor_staff',
        is_active_account=True
    )
    new_staff.set_password(password)
    # هنا نربطه بالمورد برمجياً (يمكن إضافة حقل parent_supplier_id لموديل User)
    
    db.session.add(new_staff)
    db.session.commit()
    
    return jsonify({"status": "success", "message": f"تم إضافة الموظف {username} بنجاح"})

# --- 6. حذف أو تعطيل الكيان ---
@admin_bp.route('/api/delete-sovereign-entity/<int:s_id>', methods=['DELETE'])
@login_required
@admin_required
def delete_entity(s_id):
    # لا يُسمح للموظف بهذا الإجراء أبداً
    supplier = Supplier.query.get_or_404(s_id)
    
    if float(supplier.balance_yer) > 0 or float(supplier.balance_sar) > 0:
        return jsonify({"status": "error", "message": "لا يمكن حذف كيان لديه أرصدة مالية"}), 400

    db.session.delete(supplier)
    db.session.commit()
    return jsonify({"status": "success", "message": "تم شطب الكيان نهائياً"})
