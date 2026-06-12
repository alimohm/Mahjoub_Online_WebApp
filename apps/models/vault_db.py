# coding: utf-8
# 📂 apps/models/vault_db.py - الخزنة المركزية (مُحصنة ومُشفرة بـ AES-256 - نسخة محسنة)

from apps.extensions import db
from datetime import datetime
from apps.utils.security import AESCipher
import hashlib

class AdminVault(db.Model):
    __tablename__ = 'admin_vault'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="الخزنة المركزية")
    
    # حقول مشفرة مع قيم افتراضية مشفرة لـ "0.0"
    _balance_sar = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    _balance_yer = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    _balance_usd = db.Column(db.String(255), default=lambda: AESCipher.encrypt("0.0"))
    
    integrity_hash = db.Column(db.String(64), nullable=True)

    # خصائص الوصول الآمن (Properties) مع معالجة NoneType
    @property
    def balance_sar(self): 
        val = AESCipher.decrypt(self._balance_sar)
        return float(val) if val else 0.0
    
    @balance_sar.setter
    def balance_sar(self, value): 
        self._balance_sar = AESCipher.encrypt(str(value))

    @property
    def balance_yer(self): 
        val = AESCipher.decrypt(self._balance_yer)
        return float(val) if val else 0.0
    
    @balance_yer.setter
    def balance_yer(self, value): 
        self._balance_yer = AESCipher.encrypt(str(value))

    @property
    def balance_usd(self): 
        val = AESCipher.decrypt(self._balance_usd)
        return float(val) if val else 0.0
    
    @balance_usd.setter
    def balance_usd(self, value): 
        self._balance_usd = AESCipher.encrypt(str(value))

    def generate_integrity_hash(self):
        # التحويل يستخدم الخصائص الآمنة التي تعيد أرقاماً دائماً
        data = f"{self.balance_sar}{self.balance_yer}{self.balance_usd}"
        return hashlib.sha256(data.encode()).hexdigest()

    def update_balance(self, sar_delta=0, yer_delta=0, usd_delta=0):
        self.balance_sar += sar_delta
        self.balance_yer += yer_delta
        self.balance_usd += usd_delta
        self.integrity_hash = self.generate_integrity_hash()

class VaultTransaction(db.Model):
    __tablename__ = 'vault_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    _amount = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_users.id'), nullable=True)
    reference_id = db.Column(db.String(100), nullable=True)

    @property
    def amount(self): 
        val = AESCipher.decrypt(self._amount)
        return float(val) if val else 0.0
    
    @amount.setter
    def amount(self, value): 
        self._amount = AESCipher.encrypt(str(value))
