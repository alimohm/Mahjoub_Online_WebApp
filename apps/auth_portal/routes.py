# coding: utf-8
# 📂 apps/auth_portal/routes.py - مسارات الدخول المباشر المحصنة

import os
import time
import random
from flask import render_template, request, redirect, url_for, flash, abort
from flask_login import login_user, logout_user, login_required, current_user
from apps.extensions import db
from . import auth_portal
from apps.models.admin_db import AdminUser

# مسار الدخول السري (يُجلب من إعدادات البيئة لضمان عدم كشفه في الكود)
SECRET_LOGIN_PATH = os.environ.get('ADMIN_LOGIN_PATH', '/m7jb_sovereign_hq_v2_99x')

# -------------------------------------------------------------------------
# 1. المسار السري (الدخول المباشر)
# -------------------------------------------------------------------------
@auth_portal.route(SECRET_LOGIN_PATH, methods=['GET', 'POST'])
def login():
    # منع الدخول إذا كان المستخدم مسجلاً بالفعل
    if current_user.is_authenticated:
        return redirect(url_for('admin_dashboard.dashboard'))

    if request.method == 'POST':
        # استلام آمن للبيانات
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        
        # 🛡️ الحماية من هجمات التخمين: تأخير زمني عشوائي (بين 0.8 و 1.5 ثانية)
        time.sleep(random.uniform(0.8, 1.5))
        
        # التحقق من وجود المستخدم
        user = AdminUser.query.filter_by(username=username).first()
        error_msg = 'بيانات الدخول غير صحيحة.'

        if user:
            # 🛡️ نظام القفل التصاعدي
            if hasattr(user, 'is_locked') and user.is_locked():
                flash('الحساب مقفل مؤقتاً. يرجى الانتظار.', 'danger')
            # التحقق من كلمة المرور
            elif user.check_password(password):
                if user.role in ['Owner', 'Admin']:
                    login_user(user)
                    # إعادة تعيين عداد الفشل عند النجاح
                    if hasattr(user, 'reset_failed_attempts'):
                        user.reset_failed_attempts()
                    return redirect(url_for('admin_dashboard.dashboard'))
                else:
                    flash(error_msg, 'danger')
            else:
                # تسجيل محاولة فاشلة
                if hasattr(user, 'increment_failed_attempts'):
                    user.increment_failed_attempts()
                flash(error_msg, 'danger')
        else:
            # رسالة موحدة لمنع كشف وجود المستخدم (Enumeration Attack)
            flash(error_msg, 'danger')
    
    return render_template('auth/login.html')

# -------------------------------------------------------------------------
# 2. مسار الكمين (Decoy) - لخداع البوتات
# -------------------------------------------------------------------------
@auth_portal.route('/login', methods=['GET', 'POST'])
def decoy_login():
    # 🛡️ أي محاولة وصول لهذا المسار ستؤدي لـ "حظر فوراً" (403 Forbidden)
    #
