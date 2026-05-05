# core/models/supplier.py
import os
import sys
from datetime import datetime

# --- بروتوكول حماية المسارات السيادية ---
# يضمن هذا الجزء أن Python يرى المجلد الرئيسي للمشروع كحزمة (Package)
# مما يحل مشكلة ModuleNotFoundError في Railway نهائياً
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد قاعدة البيانات من التمديدات المركزية
try:
    from core.extensions import db
except ImportError:
    # خطة بديلة في حال التشغيل من داخل مجلد core مباشرة
    try:
        from ..extensions import db
    except ImportError:
        from extensions import db

class Supplier(db.Model):
    """
    نموذج الموردين لمنظومة محجوب أونلاين
    يحتوي على كافة البيانات التجارية والمالية والجغرافية
    """
    __tablename__ = 'suppliers'
    
    # المعرفات الأساسية
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    
    # بيانات النشاط والمالك
    owner_name = db.Column(db.String(150), nullable=False)
    trade_name = db.Column(db.String(150), nullable=False)
    activity_type = db.Column(db.String(100)) # نوع النشاط (إلكترونيات، معاز، إلخ)
    
    # بيانات التوثيق (الهوية)
    id_type = db.Column(db.String(50)) # بطاقة شخصية، جواز، إلخ
    id_card_number = db.Column(db.String(50))
    id_image = db.Column(db.String(255)) # مسار صورة الهوية
    
    # بيانات الاتصال والجغرافيا (نطاق العمل: الخوخة، حيس، المخا، عدن)
    phone = db.Column(db.String(20), nullable=False)
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    address_detail = db.Column(db.Text)   # العنوان التفصيلي
    
    # الربط المالي (المحفظة السيادية)
    e_wallet = db.Column(db.String(100), unique=True) # رقم المحفظة (كريمي، أم فلوس، إلخ)
    bank_name = db.Column(db.String(100))
    bank_acc = db.Column(db.String(100))
    
    # حالة الحساب والتوقيت
    status = db.Column(db.String(20), default='active') # active, suspended, pending
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Supplier {self.trade_name} | {self.district}>'
