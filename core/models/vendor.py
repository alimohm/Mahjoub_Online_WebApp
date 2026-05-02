from core import db  # استيراد كائن db المعرف في __init__.py الخاص بـ core
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'

    # --- الحقول الأساسية ---
    id = db.Column(db.Integer, primary_key=True)
    
    # الربط مع المستخدم (User Model) - افترضنا أن اسم الجدول هو 'users'
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # --- بيانات الهوية والملك ---
    owner_name = db.Column(db.String(255), nullable=False)
    id_type = db.Column(db.String(100), nullable=False)
    id_card_number = db.Column(db.String(50), nullable=False)
    
    # --- بيانات المنشأة والنشاط ---
    trade_name = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    
    # --- البيانات الجغرافية والاتصال ---
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    address_detail = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(9), nullable=False) # التحقق يتم عادة في Form أو Logic في Flask

    # --- الربط المالي والسيادي ---
    e_wallet = db.Column(db.String(50), unique=True, nullable=True)
    fin_type = db.Column(db.String(20), default='banks')
    bank_name = db.Column(db.String(150), nullable=False)
    bank_acc = db.Column(db.String(100), nullable=False)

    # --- بيانات النظام ---
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Vendor {self.trade_name} - {self.e_wallet}>"

    # ملاحظة: في Flask-SQLAlchemy، منطق "التوليد التلقائي" للـ e_wallet 
    # يُفضل أن يتم في ملف routes.py بعد عملية الحفظ الأولية للمورد
