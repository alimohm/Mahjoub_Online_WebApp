from apps import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

# مفتاح التشفير - يجب حفظه في بيئة النظام (Environment Variable)
KEY = os.environ.get('ENCRYPTION_KEY', Fernet.generate_key().decode())
cipher_suite = Fernet(KEY.encode())

def encrypt(value):
    if value is None: return None
    return cipher_suite.encrypt(str(value).encode()).decode()

def decrypt(value):
    if value is None: return None
    return cipher_suite.decrypt(value.encode()).decode()

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    
    # حقول مشفرة لحماية الأسرار التجارية
    _encrypted_price = db.Column(db.String(500), nullable=True)
    _encrypted_cost = db.Column(db.String(500), nullable=True)
    
    status = db.Column(db.String(50), default='draft')
    quantity = db.Column(db.Integer, default=0)
    image_url = db.Column(db.String(500), nullable=True)
    supplier_id = db.Column(db.String(100), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # خصائص للوصول للبيانات (Getter & Setter)
    @property
    def price(self):
        return float(decrypt(self._encrypted_price)) if self._encrypted_price else 0.0

    @price.setter
    def price(self, value):
        self._encrypted_price = encrypt(value)

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    option1_name = db.Column(db.String(50), nullable=True)
    option1_value = db.Column(db.String(50), nullable=True)
    _encrypted_variant_price = db.Column(db.String(500), nullable=True)
    variant_quantity = db.Column(db.Integer, default=0)
    sku = db.Column(db.String(100), nullable=True)

    @property
    def variant_price(self):
        return float(decrypt(self._encrypted_variant_price)) if self._encrypted_variant_price else 0.0

    @variant_price.setter
    def variant_price(self, value):
        self._encrypted_variant_price = encrypt(value)
