import os
from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import logout_user, login_required, current_user
from sqlalchemy import or_, cast, String
from datetime import datetime

# الاستيراد من الهيكلية المعتمدة لترسانة محجوب أونلاين
from core.extensions import db 
from core.models.supplier import Supplier
from core.models.user import User

from . import admin_bp
from .auth import handle_admin_login

# --- 1. بروتوكول التحقق السيادي (حماية مركز القيادة) ---
def is_admin_sovereign():
    """ يضمن أن المؤسس علي محجوب فقط يمكنه الوصول. """
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. بوابة الدخول (The Gateway) ---
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
        suppliers_count = Supplier.query.count()
        users_count = User.query.count()
        
        # محاولة جلب عدد الطلبات إذا كان الموديل متاحاً
        try:
            from core.models.business import Order
            orders_count = Order.query.count()
        except Exception:
            orders_count = 0

        stats = {
            'suppliers_count': suppliers_count,
            'orders_count': orders_count,
            'users_count': users_count,
            'now': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        return render_template('dashboard.html', **stats)
        
    except Exception as e:
        # تسجيل الخطأ داخلياً لضمان عدم توقف الواجهة
        print(f"Dashboard Stats Error: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- 4. إدارة الموردين (عرض الصفحة) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    return render_template('manage_suppliers.html')

# --- 5. بروتوكول البحث الميداني المطور (API) ---
@admin_bp.route('/api/search-supplier', methods=['GET'])
@login_required
def api_search_supplier():
    if not is_admin_sovereign():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    query = request.args.get('q', '').strip()
    province = request.args.get('province', '').strip()
    district = request.args.get('district', '').strip()

    # إنشاء الاستعلام الأساسي
    suppliers_query = Supplier.query

    # أ) منطق البحث النصي مع معالجة النوع (Fix for image_848c92.png)
    if query and query != '*':
        # تنظيف المدخلات للبحث في المعرف الرقمي
        clean_query = query.replace('963', '').replace('SUP-MAH-', '')
        
        suppliers_query = suppliers_query.filter(
            or_(
                Supplier.trade_name.ilike(f"%{query}%"),
                Supplier.phone.ilike(f"%{query}%"),
                # تحويل النوع لضمان عدم حدوث خطأ Operator في PostgreSQL
                cast(Supplier.id, String).ilike(f"%{clean_query}%")
            )
        )

    # ب) تطبيق فلاتر الموقع الجغرافي
    if province:
        suppliers_query = suppliers_query.filter(Supplier.province == province)
    if district:
        suppliers_query = suppliers_query.filter(Supplier.district == district)

    try:
        suppliers = suppliers_query.all()
        if suppliers:
            # تحويل البيانات لـ JSON باستخدام دالة الموديل
            results = [s.to_dict() for s in suppliers]
            return jsonify({"status": "success", "suppliers": results})
        
        return jsonify({"status": "error", "message": "لم يتم العثور على نتائج"}), 404
    except Exception as e:
        # إرسال رسالة خطأ واضحة في حالة فشل الاتصال (Fix for image_ecc815.png)
        return jsonify({"status": "error", "message": f"عطل في الاتصال السيادي: {str(e)}"}), 500

# --- 6. بروتوكول تحديث بيانات المورد (Update API) ---
@admin_bp.route('/api/update-supplier/<int:sup_id>', methods=['POST'])
@login_required
def api_update_supplier(sup_id):
    if not is_admin_sovereign():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    supplier = Supplier.query.get_or_404(sup_id)
    data = request.get_json()

    try:
        # تحديث الحقول المسموح بها
        fields = ['phone', 'activity_type', 'province', 'district', 'tier', 'status']
        for field in fields:
            if field in data:
                setattr(supplier, field, data[field])

        db.session.commit()
        return jsonify({"status": "success", "message": "تم التحديث بنجاح"})
    except Exception as e:
        db.session.rollback()
        return jsonify({"status": "error", "message": str(e)}), 400

# --- 7. بروتوكول تعميد مورد جديد ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            # توليد اسم مستخدم عشوائي إذا لم يتوفر
            username = request.form.get('username') or f"user_{int(datetime.now().timestamp())}"
            
            new_supplier = Supplier(
                username=username,
                password=request.form.get('password', '123456'), # سياسة كلمة السر الافتراضية
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                id_type=request.form.get('id_type', 'شخصية'),
                id_card_number=request.form.get('id_card_number', '000'),
                address_detail=request.form.get('address_detail', 'غير محدد'),
                e_wallet=f"WAL_MAH_{int(datetime.now().timestamp())}", 
                bank_name=request.form.get('bank_name', 'غير محدد'),
                bank_acc=request.form.get('bank_acc', '000'),
                status='active',
                tier='مبتدئ'
            )
            db.session.add(new_supplier)
            db.session.commit()
            
            if is_ajax: 
                return jsonify({'status': 'success', 'message': 'تم تعميد المورد بنجاح في السجلات'})
            
            flash("تم إضافة المورد بنجاح", "success")
            return redirect(url_for('admin.manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax:
                return jsonify({'status': 'error', 'message': f"فشل التعميد: {str(e)}"}), 400
            flash(f"خطأ في الإضافة: {str(e)}", "danger")

    # حساب المعرف القادم للعرض فقط
    last_s = Supplier.query.order_by(Supplier.id.desc()).first()
    next_val = (last_s.id + 1) if last_s else 1
    return render_template('add_supplier.html', next_id=f"SUP-MAH-963{next_val}")

# --- 8. تسجيل الخروج ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم الخروج الآمن من نظام الإدارة", "info")
    return redirect(url_for('admin.login'))
