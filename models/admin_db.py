# coding: utf-8
# 🌟 استيراد المكتبات بناءً على requirements.txt المحدث
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# 🗄️ تهيئة قاعدة البيانات (تأكد من ربطها في run.py)
db = SQLAlchemy()

class AdminUser(db.Model, UserMixin):
    """
    نموذج المسؤول (AdminUser):
    يستخدم Flask-Login (عبر UserMixin) لتأمين الدخول.
    """
    __tablename__ = 'admin_users'

    # 🆔 الهوية والمفاتيح الأساسية
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    # 👤 معلومات إضافية للمسؤول
    full_name = db.Column(db.String(100), nullable=True)
    role = db.Column(db.String(20), default='super_admin') 
    
    # 🕒 سجلات النشاط (UTC لضمان دقة سجلات Railway)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)

    def set_password(self, password):
        """تشفير كلمة المرور باستخدام werkzeug"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من كلمة المرور أثناء تسجيل الدخول"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
