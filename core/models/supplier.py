from core import db
from datetime import datetime
from flask_login import UserMixin

class Supplier(db.Model, UserMixin):
    """
    موديل المورد السيادي - نظام محجوب أونلاين MAH-9046
    يجمع بين الهوية الرقمية، الحوكمة المالية، والربط بالمخزون التيهامي.
    """
    __tablename__ = 'supplier'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # --- بيانات الدخول والتعميد ---
    name = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    activity_type = db.Column(db.String(100))
    
    # --- 🛡️ نظام الرقابة والاعتماد السيادي ---
    is_approved = db.Column(db.Boolean, default=False) 
    status = db.Column(db.String(20), default='pending') # pending, active, suspended
    
    # --- تفاصيل المنشأة الجغرافية ---
    trade_name = db.Column(db.String(200))
    full_name = db.Column(db.String(200))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    phone = db.Column(db.String(20))
    email = db.Column(db.String(120), unique=True, nullable=False)

    # --- 💰 النظام المالي المتعدد (Multicurrency Wallet) ---
    wallet_balance = db.Column(db.Float, default=0.0) 
    wallet_usd = db.Column(db.Float, default=0.0)     
    wallet_sar = db.Column(db.Float, default=0.0)     
    wallet_yer = db.Column(db.Float, default=0.0)     
    
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    fin_type = db.Column(db.String(50))
    
    # استخدام timezone.utc لضمان دقة التوقيت عالمياً ومحلياً
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # --- 📦 علاقة الربط بالمخزون ---
    products = db.relationship('Product', backref='supplier_owner', lazy=True, cascade="all, delete-orphan")

    # وظيفة برمجية للتحقق من النوع داخل القوالب (Templates)
    @property
    def is_supplier(self):
        return True

    @property
    def sovereign_id(self):
        """توليد الرقم السيادي للمحفظة والتعريف الموحد"""
        return f"MAH-9046{self.id}"

    @property
    def approval_label(self):
        """تسمية الحالة السيادية لاستخدامها في واجهة المستخدم"""
        return "معتمد ✅" if self.is_approved else "بانتظار المراجعة ⏳"

    def __repr__(self):
        return f'<Supplier: {self.name} | Sovereign ID: {self.sovereign_id}>'
