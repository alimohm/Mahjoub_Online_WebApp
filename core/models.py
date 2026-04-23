from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_whatsapp = db.Column(db.String(20), unique=True, nullable=False)
    identity_url = db.Column(db.String(255))  # مسار صورة الهوية
    status = db.Column(db.String(20), default='pending')  # pending, active, suspended
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # العلاقات
    users = db.relationship('User', backref='supplier', lazy=True)
    wallet = db.relationship('Wallet', backref='supplier', uselist=False)
    products = db.relationship('Product', backref='supplier', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # owner, employee, admin
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))

class Wallet(db.Model):
    __tablename__ = 'wallets'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    balance = db.Column(db.Float, default=0.0)
    last_update = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    qumra_id = db.Column(db.String(100), unique=True)  # المعرف المرتبط بمنصة قمرة
