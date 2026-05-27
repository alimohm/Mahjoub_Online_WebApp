# coding: utf-8
import os
from apps.extensions import db
from apps.utils.security import AESCipher

cipher = AESCipher(os.getenv('ENCRYPTION_KEY', 'your-32-byte-key-here-must-be-secure'))

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
    # حقول مشفرة
    _yer_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    _sar_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    _usd_total = db.Column(db.String(255), default=cipher.encrypt("0.00"))
    
    status = db.Column(db.String(20), default='نشطة', nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.now(), nullable=False)
    updated_at = db.Column(db.DateTime, default=db.func.now(), onupdate=db.func.now(), nullable=False)

    # --- خصائص التشفير ---
    @property
    def yer_total(self): return float(cipher.decrypt(self._yer_total))
    @yer_total.setter
    def yer_total(self, val): self._yer_total = cipher.encrypt(str(val))
    # (أضف بقية الـ properties هنا)
