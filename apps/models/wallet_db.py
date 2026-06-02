# coding: utf-8
from apps.extensions import db

class Wallet(db.Model):
    __tablename__ = 'wallets'
    
    # الأعمدة الأساسية للمحفظة الرقمية
    id = db.Column(db.Integer, primary_key=True)
    wallet_code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    
    # ربط المحفظة بمعرف المورد (علاقة رأس برأس One-to-One)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id', ondelete='CASCADE'), unique=True, nullable=True)
    
    # البيانات المالية والحالة الحركية
    balance = db.Column(db.Float, default=0.0, nullable=False)
    status = db.Column(db.String(20), default='active', nullable=False)  # active, frozen, suspended
    currency = db.Column(db.String(10), default='YER', nullable=False)  # العملة الافتراضية
    
    # الطوابع الزمنية للحوكمة والتدقيق
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())

    # العلاقات البرمجية (لجلب المعاملات بسهولة)
    transactions = db.relationship('WalletTransaction', backref='wallet', lazy='dynamic', cascade='all, delete-orphan')

    def __repr__(self):
        return f"<Wallet {self.wallet_code} - Balance: {self.balance}>"


class WalletTransaction(db.Model):
    __tablename__ = 'wallet_transactions'
    
    # حقول تفاصيل الحركات المالية للتدقيق المحاسبي
    id = db.Column(db.Integer, primary_key=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('wallets.id', ondelete='CASCADE'), nullable=False)
    
    # تفاصيل الحركة المالية
    amount = db.Column(db.Float, nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # credit (إيداع/له), debit (سحب/عليه)
    
    # حقول الربط المرجعي للعمليات المركبة
    reference_id = db.Column(db.String(100), nullable=True, index=True)  # رقم الفاتورة أو السند المرتبط
    description = db.Column(db.Text, nullable=True)  # تفاصيل الحركة (شحن رصيد، تسوية، إلخ)
    
    # التوقيت الفعلي للحركة المالية من خادم قاعدة البيانات
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<Transaction {self.transaction_type} - Amount: {self.amount}>"
