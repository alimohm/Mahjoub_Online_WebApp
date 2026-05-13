# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for
from functools import wraps
import logging

# تعريف الـ Blueprint الخاص بلوحة التحكم فقط
admin_bp = Blueprint('admin_dashboard', __name__, template_folder='templates')

def login_required(f):
    """مغلف التحقق من الهوية السيادية لضمان أمن المنظومة"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/dashboard')
@login_required
def dashboard():
    """
    المحرك المركزي للوحة التحكم
    المسار: /admin/dashboard
    """
    try:
        # استدعاء ملف المحتوى الذي يرث من القالب الأساسي
        return render_template('admin/dashboard_content.html')
    except Exception as e:
        logging.error(f"خطأ في تحميل واجهة الدوشبورد: {str(e)}")
        return f"عطل فني في عرض اللوحة: {str(e)}", 500

# ملاحظة: تم إزالة دالة add_supplier من هنا لأنها تطبيق مستقل بذاته
