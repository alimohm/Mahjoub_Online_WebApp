from core import db
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    # الحقول السيادية التي أضفناها في الربط
    owner_name = db.Column(db.String(150))
    trade_name = db.Column(db.String(150))
    phone = db.Column(db.String(50))
    e_wallet = db.Column(db.String(100), unique=True) # رمز المحفظة (W-MAH-XXXX)
    
    # أرصدة الترسانة (YER, SAR, USD)
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)
    
    # توثيق زمن التعميد
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # حقول إضافية للتحقق
    id_type = db.Column(db.String(50))
    id_card_number = db.Column(db.String(100))
    address_detail = db.Column(db.Text)
