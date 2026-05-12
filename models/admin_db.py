from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

# تعريف كائن قاعدة البيانات
db = SQLAlchemy()

class AdminUser(db.Model):
    """جدول بيانات المسؤولين (الإدارة العليا)"""
    __tablename__ = 'admin_users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False) # اسم المستخدم
    password_hash = db.Column(db.String(255), nullable=False)        # كلمة السر (مشفرة)
    full_name = db.Column(db.String(100))                          # الاسم الكامل (علي محجوب)
    role = db.Column(db.String(20), default='founder')             # الدور (مؤسس/مدير)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)   # آخر ظهور

    def set_password(self, password):
        """دالة تقوم بتحويل كلمة السر العادية (مثل 123) إلى نص مشفر"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """دالة للتحقق مما إذا كانت كلمة السر المدخلة تطابق المشفرة في النظام"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<AdminUser {self.username}>'
