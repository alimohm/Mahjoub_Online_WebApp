from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    
    # الدور: 'admin' للتحكم المركز، 'supplier' للموردين
    role = db.Column(db.String(20), nullable=False, default='supplier')
    
    # حالة الحساب (نشط/محظور)
    is_active_account = db.Column(db.Boolean, default=True)

    def set_password(self, password):
        """تشفير كلمة المرور وتخزينها"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """التحقق من صحة كلمة المرور عند الدخول"""
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username} - Role: {self.role}>'
