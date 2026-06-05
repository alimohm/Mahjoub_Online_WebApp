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
    
    # الأرصدة الأساسية
    balance_sar = db.Column(db.Numeric(18, 2), default=0.0)
    balance_yer = db.Column(db.Numeric(18, 2), default=0.0)
    
    # حقل للتوقيع الأمني (Hash) للتحقق من سلامة البيانات
    # يعمل كبصمة رقمية للتأكد من أن الرصيد لم يتم التلاعب به يدوياً
    integrity_hash = db.Column(db.String(64), nullable=True)

    __table_args__ = (
        CheckConstraint('balance_sar >= 0', name='check_vault_sar_positive'),
        CheckConstraint('balance_yer >= 0', name='check_vault_yer_positive'),
    )

    def generate_integrity_hash(self):
        """إنشاء بصمة رقمية للرصيد للتحقق من عدم التلاعب"""
        data = f"{self.balance_sar}{self.balance_yer}"
        return hashlib.sha256(data.encode()).hexdigest()

    def update_balance(self, sar_delta, yer_delta):
        """دالة آمنة لتحديث الرصيد مع تحديث البصمة الأمنية"""
        self.balance_sar += sar_delta
        self.balance_yer += yer_delta
        self.integrity_hash = self.generate_integrity_hash()

class VaultTransaction(db.Model):
    __tablename__ = 'vault_transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Numeric(18, 2), nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False) # 'profit', 'fee', 'adjustment'
    description = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (
        CheckConstraint('amount != 0', name='check_transaction_amount_not_zero'),
    )
