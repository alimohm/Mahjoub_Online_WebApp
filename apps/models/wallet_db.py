# coding: utf-8
# 💳 مستند النموذج الحوكمي المطوّر للمحافظ الموحدة وسجلات التسوية - منصة محجوب أونلاين 2026
import random
from datetime import datetime
from apps.extensions import db

class SupplierWallet(db.Model):
    """ نموذج المحفظة السيادية الحاكمة لأرصدة الموردين بالعملات المتعددة """
    __tablename__ = 'supplier_wallets'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
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

    transactions = db.relationship('WalletTransaction', backref='wallet', lazy=True, cascade="all, delete-orphan")

    # ... (باقي الدوال تظل كما هي) ...

class WalletTransaction(db.Model):
    """ نظام الأرشفة والسجلات التاريخية لجميع العمليات المالية مع دعم أرباح التجزئة """
    __tablename__ = 'wallet_transactions'
    __table_args__ = {'extend_existing': True}

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    tx_code = db.Column(db.String(60), unique=True, nullable=False)
    tx_type = db.Column(db.String(30), nullable=False) 
    currency = db.Column(db.String(10), nullable=False)
    
    amount = db.Column(db.Numeric(15, 2), nullable=False)
    cost_price = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    retail_price = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    profit_margin = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    
    financial_entity = db.Column(db.String(100), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='ناجحة', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        super(WalletTransaction, self).__init__(**kwargs)
        self.update_profit()

    def update_profit(self):
        """تحديث هامش الربح بشكل صريح"""
        self.profit_margin = float(self.retail_price or 0) - float(self.cost_price or 0)

    @staticmethod
    def generate_tx_code():
        return f"TXM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"
