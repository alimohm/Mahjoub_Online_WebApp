from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Supplier(db.Model):
    """جدول الموردين - يجمع بيانات الهوية والحالة الرقابية"""
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    phone_whatsapp = db.Column(db.String(20), unique=True, nullable=False, index=True) # مفهرس للسرعة
    identity_url = db.Column(db.String(500))  # رابط الهوية في الأرشيف الخارجي
    
    # حالات المورد: pending (قيد المراجعة), active (نشط), blocked (محظور)
    status = db.Column(db.String(20), default='pending', index=True)
    region = db.Column(db.String(50))  # شمال / جنوب لضبط العملة
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # علاقات الربط
    users = db.relationship('User', backref='supplier', lazy=True)
    wallet = db.relationship('Wallet', backref='supplier', uselist=False, lazy=True)

class User(db.Model):
    """جدول المستخدمين - التمييز بين المالك والموظف"""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    
    # الرتبة: owner (مالك - يرى المحفظة), employee (موظف - تجهيز فقط)
    role = db.Column(db.String(20), default='employee') 
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

class Wallet(db.Model):
    """نظام المحفظة الذكي - القلب المالي للمنصة"""
    __tablename__ = 'wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    # الأرصدة الثلاثة (دقة محاسبية)
