# coding: utf-8
# 📂 apps/models/admin_db.py
# 🛡️ نظام إدارة هوية المالك المحصن - محجوب أونلاين 2026

from apps.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta

class AdminUser(db.Model, UserMixin):
    """
    جدول المستخدم الإداري:
    يركز على الدخول المباشر الآمن مع حماية ضد التخمين (Brute Force).
    """
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    phone_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(50), default='admin')
    is_active = db.Column(db.Boolean, default=True)
    
    # 🔒 حقول الحماية الأمنية ضد الاختراق
    failed_attempts = db.Column(db.Integer, default=0)
    lock_until = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """تشفير كلمة المرور قبل التخزين"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من صحة كلمة المرور المدخلة"""
        return check_password_hash(self.password_hash, password)

    # 🛡️ منطق الحماية التصاعدية (منع هجمات التخمين)
    def is_locked(self):
        """التحقق من حالة القفل في السيرفر"""
        if self.lock_until and datetime.utcnow() < self.lock_until:
            return True
        return False

    def increment_failed_attempts(self):
        """زيادة عداد الفشل وتمديد وقت القفل"""
        self.failed_attempts += 1
        # القفل يزداد بمرور الوقت لمنع الهجمات الآلية
        delay = (self.failed_attempts // 5) + 1 
        self.lock_until = datetime.utcnow() + timedelta(minutes=delay)
        # تمت إزالة db.session.commit() من هنا لتفادي التعارض مع الـ route

    def reset_failed_attempts(self):
        """إعادة تعيين العداد عند النجاح"""
        self.failed_attempts = 0
        self.lock_until = None
        # تمت إزالة db.session.commit() من هنا لتفادي التعارض مع الـ route

    def __repr__(self):
        return f'<AdminUser {self.username}>'
