# coding: utf-8
# 📂 apps/models/bridge_db.py

from apps import db
from datetime import datetime
from cryptography.fernet import Fernet
import os

# --- قسم التشفير ---
def get_cipher_suite():
    """الحصول على المفتاح من البيئة وتهيئته بشكل صحيح"""
    key = os.environ.get('ENCRYPTION_KEY')
    if key:
        try:
            return Fernet(key.encode('utf-8'))
        except Exception as e:
            print(f"❌ خطأ في مفتاح التشفير: {e}")
            raise ValueError("ENCRYPTION_KEY غير صالح.")
    
    return Fernet(Fernet.generate_key())

cipher_suite = get_cipher_suite()

def encrypt(value):
    if value is None: return None
    return cipher_suite.encrypt(str(value).encode('utf-8')).decode('utf-8')

def decrypt(value):
    if value is None: return None
    try:
        return cipher_suite.decrypt(value.encode('utf-8')).decode('utf-8')
    except Exception:
        return "0.0"

# --- قسم الموديلات ---
class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    image_url = db.Column(db.String(500)) 
    _price = db.Column(db.Text, nullable=False) 
    quantity = db.Column(db.Integer, default=0)
    supplier_id = db.Column(db.String(100))
    sku = db.Column(db.String(100)) 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def price(self):
        return decrypt(self._price)

    @price.setter
    def price(self, value):
        self._price = encrypt(value)

class ProductVariant(db.Model):
    __tablename__ = 'product_variants'
    id = db.Integer, primary_key=True
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    sku = db.Column(db.String(100))
    _price = db.Column(db.Text) 

    @property
    def price(self):
        return decrypt(self._price)

    @price.setter
    def price(self, value):
        self._price = encrypt(value)
