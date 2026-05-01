from core import db
from datetime import datetime

class Product(db.Model):
    """
    موديل المنتجات - الترسانة التجارية لمنصة محجوب أونلاين.
    """
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # تفاصيل السعر والعملة السيادية
    price = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='SAR') 
    
    # التصنيفات (ملابس، أدوات منزلية، إلخ)
    category = db.Column(db.String(100), nullable=False)
    
    # المخزون وحالة التوفر
    stock_quantity = db.Column(db.Integer, default=0)
    is_available = db.Column(db.Boolean, default=True)
    
    # مسار الصورة
    image_url = db.Column(db.String(500), nullable=True)
    
    # الربط مع المورد (User)
    supplier_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # التوقيت
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Product {self.name}>'
