from core import db
from datetime import datetime
from flask_login import UserMixin

# جدول الإدارة العليا (القائد والمراقبين)
class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default='admin') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# جدول شركاء النجاح (الموردين)
class Supplier(db.Model, UserMixin):
    __tablename__ = 'supplier'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=True) 
    phone = db.Column(db.String(20), nullable=True)
    
    # محفظة المورد (الرصيد المالي المرتبط بالآيدي)
    wallet_balance = db.Column(db.Float, default=0.0) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # علاقة الربط مع المنتجات
    products = db.relationship('Product', backref='owner', lazy=True)

# جدول ترسانة المنتجات (الربط بين الإدارة والمورد وقمرة)
class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    
    # الحقول المالية والربط الذكي
    original_price = db.Column(db.Float, nullable=False, default=0.0) # سعر المورد (التكلفة)
    sale_price = db.Column(db.Float, nullable=False, default=0.0)     # سعرك في "قمرة"
    
    image_url = db.Column(db.String(500), nullable=True)
    description = db.Column(db.Text, nullable=True)
    
    # حالة المزامنة (هل المنتج مسحوب ومعروض في المتجر؟)
    is_synced = db.Column(db.Boolean, default=False)
    status = db.Column(db.String(50), default='active') 
    
    # الربط بهوية المورد (ID)
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name} | Supplier ID: {self.supplier_id}>'
