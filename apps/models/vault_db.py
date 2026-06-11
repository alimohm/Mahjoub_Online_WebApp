# coding: utf-8
# 📂 apps/models/vault_db.py - الخزنة المركزية (مُشفرة ومُحصنة)

from apps.extensions import db
from datetime import datetime
from sqlalchemy import CheckConstraint
import hashlib

class AdminVault(db.Model):
    __tablename__ = 'admin_vault'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), default="الخزنة المركزية")
    
    # الأرصدة الأساسية (تم استخدام Numeric للدقة المحاسبية)
    balance_sar = db.Column(db.Numeric(18, 2), default=0.0)
    balance_yer = db.Column(db.Numeric(18, 2), default=0.0)
    balance_usd = db.Column(db.Numeric(18, 2), default=0.0)
    
    # حقل للتوقيع الأمني (Hash) للتحقق من سلامة البيانات
    integrity_hash = db.Column(db.String(64), nullable=True)

    __table_args__ = (
        CheckConstraint('balance_sar >= 0', name='check_vault_sar_positive'),
        CheckConstraint('balance_yer >= 0', name='check_vault_yer_positive'),
        CheckConstraint('balance_usd >= 0', name='check_vault_usd_positive'),
    )

    def generate_integrity_hash(self):
        """إنشاء بصمة رقمية للرصيد للتحقق من عدم التلاعب"""
        data = f"{self.balance_sar}{self.balance_yer}{self.balance_usd}"
        return hashlib.sha256(data.encode()).hexdigest()

    def update_balance(self, sar_delta=0, yer_delta=0, usd_delta=0):
        """تحديث آمن للأرصدة مع تجديد البصمة الأمنية"""
        self.balance_sar += sar_delta
        self.balance_yer += yer_delta
        self.balance_usd += usd_delta
        self.integrity_hash = self.generate_integrity_hash()

class VaultTransaction(db.Model):
    __tablename__ = 'vault_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # تفاصيل العملية
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False) # SAR, YER, USD
    transaction_type = db.Column(db.String(50), nullable=False) # 'deposit', 'withdrawal', 'profit_cut'
    description = db.Column(db.String(255))
    
    # روابط التتبع
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin_user.id'), nullable=True)
    
    # مرجع خارجي (لربط العملية برقم حركة في المحفظة أو المورد)
    reference_id = db.Column(db.String(100), nullable=True)

    __table_args__ = (
        CheckConstraint('amount != 0', name='check_transaction_amount_not_zero'),
    )

    def __repr__(self):
        return f'<VaultTransaction {self.transaction_type} {self.amount} {self.currency}>'
