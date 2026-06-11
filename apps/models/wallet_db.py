# coding: utf-8
# 📂 apps/models/wallet_db.py - نظام المحافظ (مُشفر بالكامل بـ AES-256)

from apps.extensions import db
from apps.utils.security import AESCipher
from datetime import datetime

class SupplierWallet(db.Model):
    __tablename__ = 'supplier_wallets'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, unique=True)
    supplier = db.relationship('Supplier', back_populates='wallet')
    
    # حقول مشفرة (تخزن كـ String في قاعدة البيانات)
    _balance_sar = db.Column(db.String(255), default="0.0")
    _balance_yer = db.Column(db.String(255), default="0.0")
    _balance_usd = db.Column(db.String(255), default="0.0")
    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # خصائص التشفير التلقائي (Properties)
    @property
    def balance_sar(self): 
        return float(AESCipher.decrypt(self._balance_sar))
    
    @balance_sar.setter
    def balance_sar(self, value): 
        self._balance_sar = AESCipher.encrypt(str(value))

    @property
    def balance_yer(self): 
        return float(AESCipher.decrypt(self._balance_yer))
    
    @balance_yer.setter
    def balance_yer(self, value): 
        self._balance_yer = AESCipher.encrypt(str(value))

    @property
    def balance_usd(self): 
        return float(AESCipher.decrypt(self._balance_usd))
    
    @balance_usd.setter
    def balance_usd(self, value): 
        self._balance_usd = AESCipher.encrypt(str(value))

    transactions = db.relationship('WalletTransaction', back_populates='wallet', lazy='dynamic')

    def add_transaction(self, amount, currency, transaction_type, description=None):
        transaction = WalletTransaction(
            wallet_id=self.id,
            amount=amount, # يتم التشفير تلقائياً عبر الـ setter في الكلاس أدناه
            currency=currency.upper(),
            transaction_type=transaction_type,
            description=description
        )
        
        multiplier = 1 if transaction_type == 'credit' else -1
        
        # تحديث الأرصدة (تستخدم الـ setter التي تشفر القيمة)
        if currency.upper() == 'SAR': self.balance_sar += (amount * multiplier)
        elif currency.upper() == 'YER': self.balance_yer += (amount * multiplier)
        elif currency.upper() == 'USD': self.balance_usd += (amount * multiplier)
            
        db.session.add(transaction)
        db.session.commit()
        return transaction

class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    wallet = db.relationship('SupplierWallet', back_populates='transactions')
    
    # حقل مشفر
    _amount = db.Column(db.String(255), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)
    description = db.Column(db.String(255))
    status = db.Column(db.String(20), default='completed') 
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    @property
    def amount(self): 
        return float(AESCipher.decrypt(self._amount))
    
    @amount.setter
    def amount(self, value): 
        self._amount = AESCipher.encrypt(str(value))
