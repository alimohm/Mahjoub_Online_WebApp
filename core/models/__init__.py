from datetime import datetime
from flask_login import UserMixin
# استيراد db من النواة المركزية لضمان وحدة المحرك السيادي
from core import db

# --- 1. جدول المستخدمين الموحد (الاسم، كلمة السر، الرتبة) ---
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin') # admin أو supplier
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة لربط المستخدم ببروفايل المورد (إذا كان حسابه مورد)
    supplier_profile = db.relationship('Supplier', backref='user_account', uselist=False)

# --- 2. جدول الموردين (التفاصيل التجارية والمحافظ) ---
class Supplier(db.Model):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    # ربط البروفايل بحساب المستخدم الأساسي
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    trade_name = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(20), nullable=True)
    province = db.Column(db.String(50), nullable=True) # مثل: الحديدة
    
    # المحافظ السيادية (YER, SAR, USD)
    wallet_balance = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_usd = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_sar = db.Column(db.Numeric(10, 2), default=0.00)
    wallet_yer = db.Column(db.Numeric(10, 2), default=0.00)
    
    is_approved = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(20), default='pending')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة مع المنتجات
    products = db.relationship('Product', backref='supplier', lazy=True, cascade="all, delete-orphan")

# --- 3. جدول المنتجات (الربط مع قمرة والأسعار) ---
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    q_product_id = db.Column(db.String(100), unique=True, nullable=True) # ID المنتج في قمرة
    q_collection_id = db.Column(db.String(100), nullable=True) # القسم
    
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    cost_price = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    sale_price = db.Column(db.Numeric(10, 2), nullable=True)
    
    status = db.Column(db.String(50), default='pending') # pending, active
    is_active = db.Column(db.Boolean, default=False)
    is_synced = db.Column(db.Boolean, default=False)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
