# coding: utf-8
# 💳 مستند النموذج الحوكمي المطوّر للمحافظ الموحدة وسجلات التسوية - منصة محجوب أونلاين 2026
import random
from datetime import datetime
from apps.extensions import db

class SupplierWallet(db.Model):
    """ نموذج المحفظة السيادية الحاكمة لأرصدة الموردين بالعملات المتعددة """
    __tablename__ = 'supplier_wallets'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    supplier_id = db.Column(db.String(50), db.ForeignKey('suppliers.sovereign_id'), nullable=False, unique=True)
    wallet_code = db.Column(db.String(50), nullable=False, unique=True)
    
    # 🇾🇪 أرصدة الريال اليمني (YER)
    yer_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    yer_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    yer_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    # 🇸🇦 أرصدة الريال السعودي (SAR)
    sar_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    sar_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    sar_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    # 🇺🇸 أرصدة الدولار الأمريكي (USD)
    usd_total = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    usd_withdrawn = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)
    usd_pending = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)

    status = db.Column(db.String(20), default='نشطة', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)

    transactions = db.relationship('WalletTransaction', backref='wallet', lazy=True, cascade="all, delete-orphan")

    @staticmethod
    def generate_next_wallet_code():
        last_wallet = SupplierWallet.query.order_by(SupplierWallet.id.desc()).first()
        if last_wallet and last_wallet.wallet_code:
            try:
                parts = last_wallet.wallet_code.split('MAH963')
                last_num = int(parts[-1])
                return f"WEL-MAH963{last_num + 1}"
            except (ValueError, IndexError):
                return f"WEL-MAH963{random.randint(100, 999)}"
        return "WEL-MAH9631"

    @property
    def yer_available(self):
        return max(0.00, float(self.yer_total - self.yer_withdrawn - self.yer_pending))

    @property
    def sar_available(self):
        return max(0.00, float(self.sar_total - self.sar_withdrawn - self.sar_pending))

    @property
    def usd_available(self):
        return max(0.00, float(self.usd_total - self.usd_withdrawn - self.usd_pending))

    def __repr__(self):
        return f"<SupplierWallet {self.wallet_code} | Supplier {self.supplier_id}>"


class WalletTransaction(db.Model):
    """ نظام الأرشفة والسجلات التاريخية لجميع العمليات المالية مع دعم أرباح التجزئة """
    __tablename__ = 'wallet_transactions'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    wallet_id = db.Column(db.Integer, db.ForeignKey('supplier_wallets.id'), nullable=False)
    
    tx_code = db.Column(db.String(60), unique=True, nullable=False)
    tx_type = db.Column(db.String(30), nullable=False) 
    currency = db.Column(db.String(10), nullable=False)
    
    # 📉 البيانات المالية للعملية
    amount = db.Column(db.Numeric(15, 2), nullable=False) # المبلغ الصافي للحركة
    cost_price = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)    # سعر التكلفة (جملة)
    retail_price = db.Column(db.Numeric(15, 2), default=0.00, nullable=False)  # سعر البيع (تجزئة)
    profit_margin = db.Column(db.Numeric(15, 2), default=0.00, nullable=False) # هامش الربح (تلقائي)
    
    financial_entity = db.Column(db.String(100), nullable=True)
    reference_number = db.Column(db.String(100), nullable=True)
    notes = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), default='ناجحة', nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def __init__(self, **kwargs):
        super(WalletTransaction, self).__init__(**kwargs)
        # حساب الربح تلقائياً عند إنشاء أي عملية
        self.profit_margin = float(self.retail_price) - float(self.cost_price)

    @staticmethod
    def generate_tx_code():
        return f"TXM-{datetime.utcnow().strftime('%Y%m%d%H%M%S')}-{random.randint(1000, 9999)}"

    def __repr__(self):
        return f"<WalletTransaction {self.tx_code} | Profit {self.profit_margin} {self.currency}>"
