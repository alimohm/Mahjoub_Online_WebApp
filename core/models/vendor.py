from core import db  # استيراد كائن db المعرف في __init__.py الخاص بـ core
from datetime import datetime

class Vendor(db.Model):
    __tablename__ = 'vendors'

    # --- الحقول الأساسية ---
    id = db.Column(db.Integer, primary_key=True)
    
    # الربط مع المستخدم (User Model)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # --- بيانات الهوية والملك والوثائق ---
    owner_name = db.Column(db.String(255), nullable=False)
    id_type = db.Column(db.String(100), nullable=False)
    id_card_number = db.Column(db.String(50), nullable=False)
    
    # الحقل الجديد: تخزين مسار صورة الهوية أو السجل التجاري
    id_image_path = db.Column(db.String(500), nullable=True) 
    
    # --- بيانات المنشأة والنشاط ---
    trade_name = db.Column(db.String(255), nullable=False)
    activity_type = db.Column(db.String(100), nullable=False)
    
    # --- البيانات الجغرافية والاتصال ---
    # ملاحظة: تعتمد العمليات في الخوخة، عدن، المخاء، وحيس على هذه البيانات
    province = db.Column(db.String(100), nullable=False)
    district = db.Column(db.String(100), nullable=False)
    address_detail = db.Column(db.String(500), nullable=False)
    phone = db.Column(db.String(15), nullable=False) # تم زيادة الطول لمرونة أكبر مع المفاتيح الدولية

    # --- الربط المالي والسيادي ---
    # يعكس هذا القسم رؤيتك لبناء النجاح على الثقة والأنظمة الرقمية
    e_wallet = db.Column(db.String(50), unique=True, nullable=True)
    fin_type = db.Column(db.String(20), default='banks')
    bank_name = db.Column(db.String(150), nullable=False)
    bank_acc = db.Column(db.String(100), nullable=False)

    # --- بيانات النظام ---
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_verified = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<Vendor {self.trade_name} - {self.e_wallet}>"
