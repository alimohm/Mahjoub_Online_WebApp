# coding: utf-8
# 📂 apps/models/admin_db.py
# 🛡️ نظام إدارة هوية المالك - محجوب أونلاين 2026

from apps.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class AdminUser(db.Model, UserMixin):
    """
    جدول المستخدم الإداري: يحتوي على بيانات الدخول الأساسية 
    مع دعم التحقق الثنائي (2FA) عبر رقم الهاتف.
    """
    __tablename__ = 'admin_users'
    
    # المعرف الفريد للمستخدم
    id = db.Column(db.Integer, primary_key=True)
    
    # اسم المستخدم
    username = db.Column(db.String(100), unique=True, nullable=False)
    
    # كلمة المرور المشفرة (تُخزن كـ Hash قوي)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # رقم الهاتف المعتمد لعمليات الـ 2FA (WhatsApp)
    phone_number = db.Column(db.String(20), nullable=False)
    
    # صلاحيات النظام
    role = db.Column(db.String(50), default='admin')
    
    # حالة التفعيل للتحكم في الوصول
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """تشفير كلمة المرور قبل التخزين (Hashing)"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من صحة كلمة المرور المدخلة"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
