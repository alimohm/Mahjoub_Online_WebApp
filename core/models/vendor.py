# core/models/vendor.py

class Vendor(db.Model):
    __tablename__ = 'vendors'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    
    # الحقول الأساسية التي أضفتها أنت سابقاً
    trade_name = db.Column(db.String(150))
    owner_name = db.Column(db.String(150))
    e_wallet = db.Column(db.String(100), unique=True) # الرقم السيادي للمحفظة
    
    # --- الأعمدة المالية المطلوبة (أضفها إذا لم تكن موجودة) ---
    balance_yer = db.Column(db.Float, default=0.0) # رصيد ريال يمني
    balance_sar = db.Column(db.Float, default=0.0) # رصيد ريال سعودي
    balance_usd = db.Column(db.Float, default=0.0) # رصيد دولار أمريكي
    
    created_at = db.Column(db.DateTime, default=db.func.now())
    # ... بقية الحقول (الهاتف، المحافظة، إلخ)
