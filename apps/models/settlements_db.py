# coding: utf-8
# 📂 apps/models/settlements_db.py
import random
from datetime import datetime
from apps.extensions import db

class AdminSettlement(db.Model):
    """
    جدول مخصص مستقل حصرياً لإدارة وتوثيق التسويات المالية الإدارية.
    """
    __tablename__ = 'admin_settlements'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    
    # الربط مع المحفظة
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    wallet_code = db.Column(db.String(50), nullable=False)
    
    # الربط البرمجي للوصول لبيانات المورد (Supplier) من خلال المحفظة
    wallet = db.relationship('SupplierWallet', backref=db.backref('settlements', lazy=True))
    
    # تفاصيل السند
    settlement_code = db.Column(db.String(60), unique=True, nullable=False)
    settlement_type = db.Column(db.String(30), nullable=False) # إيداع / خصم
    currency = db.Column(db.String(10), nullable=False)
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    
    # تفاصيل الحوكمة
    financial_entity = db.Column(db.String(100), default="إدارة المنصة المركزية", nullable=True)
    reference_number = db.Column(db.String(100), default="SETTLE-ADMIN", nullable=True)
    reason_notes = db.Column(db.Text, nullable=False)
    created_by = db.Column(db.String(50), nullable=True)
    
    # الحالة (مهمة للفلترة في الجدول الجديد)
    status = db.Column(db.String(20), default='منفذة', nullable=False) # منفذة / معلقة / ملغاة
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    @staticmethod
    def generate_settlement_code():
        return f"STL-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

    def __repr__(self):
        return f"<AdminSettlement {self.settlement_code} | {self.status}>"
