# coding: utf-8
# 🛡️ موديل إدارة المتحكمين - منصة محجوب أونلاين
# التوثيق: هذا الملف يحدد هيكلية جدول المدير (Admin) في قاعدة البيانات

from apps import db, login_manager
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    """دالة لتحميل المستخدم من قاعدة البيانات بواسطة المعرف الشخصي"""
    return AdminUser.query.get(int(user_id))

class AdminUser(db.Model, UserMixin):
    """
    كلاس AdminUser: المسؤول عن تخزين بيانات إدارة المنصة.
    الاسم تم توحيده ليتناسب مع ملفات التشغيل (run.py).
    """
    __tablename__ = 'admin_users' # تسمية الجدول في قاعدة البيانات

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # حقول إضافية لمراقبة النشاط السيادي
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """تشفير كلمة المرور قبل تخزينها لضمان الأمان"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من صحة كلمة المرور المدخلة"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
