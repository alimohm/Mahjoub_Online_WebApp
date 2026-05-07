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
        print(f"❌ Dashboard Stats Error: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, now=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# --- 4. إدارة الموردين (عرض الصفحة الرئيسية مع الفلاتر الجغرافية) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    # قائمة الجغرافيا المركزية لضمان تقليل الأكواد في الفلاتر
    yemen_geography = {
        "الحديدة": ["الخوخة", "حيس", "الحوك", "الميناء", "زبيد", "بيت الفقيه"],
        "أمانة العاصمة": ["السبعين", "التحرير", "الثورة", "صنعاء القديمة"],
        "عدن": ["المنصورة", "كريتر", "الشيخ عثمان", "البريقة"],
        "تعز": ["المخاء", "القاهرة", "المظفر"]
    }

    # جلب قائمة أولية مرتبة حسب الأحدث
    all_suppliers = Supplier.query.order_by(Supplier.id.desc()).all()
    
    return render_template('manage_suppliers.html', 
                           suppliers=all_suppliers, 
                           provinces_list=yemen_geography.keys())

# --- 5. بروتوكول البحث الميداني المطور (الاستجابة الذكية للفلاتر) ---
@admin_bp.route('/api/search-supplier', methods=['GET'])
@login_required
def api_search_supplier():
    if not is_admin_sovereign():
        return jsonify({"status": "error", "message": "Unauthorized Access"}), 403

    query = request.args.get('q', '').strip()
    province = request.args.get('province', '').strip()
    district = request.args.get('district', '').strip()

    suppliers_query = Supplier.query

    # أ) منطق البحث النصي الذكي
    if query:
        clean_query = query.replace('SUP-MAH-', '').replace('WAL-MAH-', '')
        suppliers_query = suppliers_query.filter(
            or_(
                Supplier.trade_name.ilike(f"%{query}%"),
                Supplier.phone.ilike(f"%{query}%"),
                Supplier.owner_name.ilike(f"%{query}%"),
                Supplier.e_wallet.ilike(f"%{query}%"),
                cast(Supplier.id, String).ilike(f"%{clean_query}%")
            )
        )

    # ب) الفلترة الجغرافية
    if province:
        suppliers_query = suppliers_query.filter(Supplier.province == province)
    if district:
        suppliers_query = suppliers_query.filter(Supplier.district == district)

    try:
        suppliers = suppliers_query.order_by(Supplier.id.desc()).all()
        results = [s.to_dict() for s in suppliers]
        return jsonify({
            "status": "success", 
            "count": len(results),
            "suppliers": results
        })
    except Exception as e:
        return jsonify({"status": "error", "message": f"عطل في الاتصال السيادي: {str(e)}"}), 500

# --- 6. بروتوكول تحديث الحالة والبيانات (التحكم في المورد) ---
@admin_bp.route('/api/update-supplier-status/<int:sup_id>', methods=['POST'])
@login_required
def update_status(sup_id):
    if not is_admin_sovereign():
        return jsonify({"status": "error", "message": "Unauthorized"}), 403

    supplier = Supplier.query.get_or_404(sup_id)
    data = request.get_json()
    new_status = data.get('status')

    if new_status in ['active', 'suspended']:
        supplier.status = new_status
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تحديث حالة {supplier.trade_name} إلى {new_status}"})
    
    return jsonify({"status": "error", "message": "حالة غير معروفة"}), 400

# --- 7. بروتوكول تعميد مورد جديد ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): 
        return redirect(url_for('admin.login'))
    
    if request.method == 'POST':
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        try:
            # إنشاء كائن المورد الجديد
            new_supplier = Supplier(
                username=request.form.get('username'),
                password=request.form.get('password', '123456'),
                owner_name=request.form.get('owner_name'),
                trade_name=request.form.get('trade_name'),
                activity_type=request.form.get('activity_type'),
                phone=request.form.get('phone'),
                province=request.form.get('province'),
                district=request.form.get('district'),
                id_type=request.form.get('id_type'),
                id_card_number=request.form.get('id_card_number'),
                address_detail=request.form.get('address_detail'),
                bank_name=request.form.get('bank_name'),
                bank_acc=request.form.get('bank_acc'),
                status='active',
                tier='مبتدئ'
            )
            
            db.session.add(new_supplier)
            db.session.flush() # للحصول على الـ ID قبل الـ commit
            
            # نقش المعرف السيادي والمحفظة آلياً
            new_supplier.mint_sovereign_id()
            
            db.session.commit()
            
            if is_ajax: 
                return jsonify({'status': 'success', 'message': f'تم تعميد المورد بنجاح بالمعرف السيادي: {new_supplier.e_wallet}'})
            
            flash("تم إضافة المورد بنجاح", "success")
            return redirect(url_for('admin.manage_suppliers'))
            
        except Exception as e:
            db.session.rollback()
            if is_ajax:
                return jsonify({'status': 'error', 'message': f"فشل التعميد: {str(e)}"}), 400
            flash(f"خطأ: {str(e)}", "danger")

    last_s = Supplier.query.order_by(Supplier.id.desc()).first()
    next_id_val = (last_s.id + 1) if last_s else 1
    return render_template('add_supplier.html', next_id=f"963{next_id_val}")

# --- 8. تسجيل الخروج الآمن ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة السيادية بنجاح", "info")
    return redirect(url_for('admin.login'))
