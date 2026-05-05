import os
from flask import render_template, request, redirect, url_for, flash
from flask_login import logout_user, login_required, current_user
from sqlalchemy import text
from core import db 
from . import admin_bp
from .auth import handle_admin_login

# --- 1. التحقق من الصلاحية (علي محجوب فقط) ---
# نضمن أن الوصول مقتصر على رتبة 'admin' فقط لضمان السيادة
def is_admin_sovereign():
    return current_user.is_authenticated and getattr(current_user, 'role', '').lower() == 'admin'

# --- 2. مركز القيادة (الداشبورد المصفح) ---
@admin_bp.route('/')
@admin_bp.route('/dashboard')
@login_required
def admin_dashboard():
    if not is_admin_sovereign():
        return redirect(url_for('main.index'))
    
    try:
        # استعلامات مباشرة (Direct SQL) لتجنب انهيار الموديلات
        # إحصائيات الموردين من المستخدمين ذوي رتبة 'vendor'
        suppliers = db.session.execute(text("SELECT COUNT(*) FROM users WHERE role = 'vendor'")).scalar() or 0
        total_users = db.session.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        
        # تجنب الانهيار في حال لم يُنشأ جدول الطلبات بعد أو كان قيد التحديث
        try:
            total_orders = db.session.execute(text("SELECT COUNT(*) FROM orders")).scalar() or 0
        except Exception:
            total_orders = 0

        stats = {
            'suppliers_count': suppliers,
            'orders_count': total_orders,
            'users_count': total_users,
            'pending_withdrawals': 0 # سيتم ربطها بنظام المحافظ لاحقاً
        }
        # تم الربط مع dashboard.html الذي يستقبل هذه المتغيرات
        return render_template('dashboard.html', **stats)
        
    except Exception as e:
        # نظام الحماية من الانهيار (Crash Avoidance)
        print(f"⚠️ Dashboard Crash Avoided: {str(e)}")
        return render_template('dashboard.html', suppliers_count=0, orders_count=0, users_count=0, pending_withdrawals=0)

# --- 3. إدارة الموردين (حوكمة الكيانات) ---
@admin_bp.route('/manage-suppliers')
@login_required
def manage_suppliers():
    if not is_admin_sovereign(): 
        return redirect(url_for('main.index'))
    
    try:
        # جلب قائمة الموردين المعتمدين في محجوب أونلاين
        result = db.session.execute(text("SELECT id, username, email, is_active_account FROM users WHERE role = 'vendor'"))
        suppliers = result.fetchall()
        return render_template('manage_suppliers.html', suppliers=suppliers)
    except Exception as e:
        flash(f"خطأ في جلب بيانات الموردين: {str(e)}", "danger")
        return redirect(url_for('admin.admin_dashboard'))

# --- 4. نظام الدخول الآمن ---
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    # إذا كان المستخدم أدمن بالفعل، يتم توجيهه مباشرة للمركز
    if is_admin_sovereign(): 
        return redirect(url_for('admin.admin_dashboard'))
    return handle_admin_login()

# --- 5. إنهاء الجلسة السيادية ---
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم إنهاء الجلسة الآمنة بنجاح", "info")
    return redirect(url_for('admin.login'))

# --- 6. مسارات إضافية (قيد التطوير) ---
@admin_bp.route('/add-supplier', methods=['GET', 'POST'])
@login_required
def add_supplier():
    if not is_admin_sovereign(): return redirect(url_for('main.index'))
    # هنا يتم إضافة منطق تعميد مورد جديد لاحقاً
    return render_template('add_supplier.html')
