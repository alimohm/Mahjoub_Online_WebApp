# coding: utf-8
from datetime import datetime
from apps import db

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
    # الأعمدة الفعلية (يجب استخدام هذه في الـ routes.py)
    yer_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    yer_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    yer_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    sar_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    sar_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    sar_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    usd_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    usd_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    usd_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    status = db.Column(db.String(20), default='نشطة', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<SupplierWallet {self.wallet_code}>"
