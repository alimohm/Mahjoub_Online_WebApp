# core/models/supplier.py
from datetime import datetime
from flask_login import UserMixin
from core.extensions import db

class Supplier(db.Model, UserMixin):
    """ موديل المورد الأساسي """
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    
    trade_name = db.Column(db.String(150), nullable=False)
    owner_name = db.Column(db.String(150))
    activity_type = db.Column(db.String(100))
    identity_type = db.Column(db.String(50))
    identity_image = db.Column(db.String(255))
    
    phone = db.Column(db.String(20))
    email = db.Column(db.String(150))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
    
    bank_name = db.Column(db.String(150))
    bank_acc = db.Column(db.String(100))
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)
    
    status = db.Column(db.String(20), default='active')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Supplier {self.trade_name}>"

# --- تأكد من وجود هذا الجزء بالأسفل ---
class SupplierStaff(db.Model):
    """ طاقم العمل التابع للمورد """
    __tablename__ = 'supplier_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100)) # مدير، مندوب، محاسب
    status = db.Column(db.String(20), default='active')
    
    # علاقة الربط
    supplier = db.relationship('Supplier', backref=db.backref('staff_members', lazy=True))
