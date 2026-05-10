# admin_panel/routes.py
from flask import render_template, redirect, url_for, flash
from flask_login import login_required, logout_user
from core import db
from core.models.user import User
from core.models.supplier import Supplier
from datetime import datetime

# 1. استيراد البلوبرنت
from . import admin_bp
from .auth import login_view 

# ==========================================
# 1. بوابة الولوج (The Login Gate)
# ==========================================
@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    return login_view()

# ==========================================
# 2. غرفة القيادة (Dashboard)
# ==========================================
@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """عرض إحصائيات النظام الأساسية فقط"""
    try:
        data = {
            'users_count': User.query.count(),
            'suppliers_count': Supplier.query.count(),
            'orders_count': 0, 
            
            # رصد السيولة في قاعدة البيانات المحلية
            'total_yer': db.session.query(db.func.sum(Supplier.balance_yer)).scalar() or 0.0,
            'total_sar': db.session.query(db.func.sum(Supplier.balance_sar)).scalar() or 0.0,
            'total_usd': db.session.query(db.func.sum(Supplier.balance_usd)).scalar() or 0.0,
            
            'now': datetime.now()
        }
        return render_template('admin/dashboard.html', **data)
    except Exception as e:
        # إذا حدث خطأ هنا، سيظهر كرسالة نصية بدلاً من انهيار السيرفر بالكامل
        return f"⚠️ خطأ في الرادار: {e}"

# ==========================================
# 3. إدارة الموردين (Suppliers)
# ==========================================
@admin_bp.route('/suppliers')
@login_required
def manage_suppliers():
    """عرض الموردين المسجلين في النظام المحلي"""
    try:
        # جلب آخر 20 مورد مباشرة
        suppliers = Supplier.query.order_by(Supplier.id.desc()).limit(20).all()
        
        # --- تعديل طوارئ هنا لمنع انهيار السيرفر ---
        # بما أن السجلات أظهرت أن "tier" غير موجود في قاعدة البيانات حالياً
        # سنقوم بتعطيل الفلترة به حتى تقوم بتحديث الـ Model
        stats = {
            'total': Supplier.query.count(),
            'active': Supplier.query.filter_by(status='active').count(),
            'sovereign': 0  # اجعلها 0 مؤقتاً لتجاوز خطأ
        }
        
        return render_template('admin/manage_suppliers.html', 
                               suppliers=suppliers, 
                               stats=stats)
    except Exception as e:
        return f"⚠️ خطأ في إدارة الموردين: {e}"

# ==========================================
# 4. بروتوكول الخروج الآمن (Logout)
# ==========================================
@admin_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("تم تسجيل الخروج. النظام في وضع الحماية.", "info")
    return redirect(url_for('admin.login'))
