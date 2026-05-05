# core/models/supplier.py
import os
import sys
from datetime import datetime

# --- بروتوكول تثبيت المسارات (Railway Patch) ---
# هذا الجزء يضمن إخبار السيرفر بمكان وجود المجلد الرئيسي للمشروع
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '..', '..'))

if project_root not in sys.path:
    sys.path.insert(0, project_root)

# استيراد db باستخدام مسار مرن يتكيف مع السيرفر لضمان العمل على Railway
try:
    from core.extensions import db
except (ImportError, ModuleNotFoundError):
    try:
        from extensions import db
    except (ImportError, ModuleNotFoundError):
        from ..extensions import db

class Supplier(db.Model):
    """
    نموذج الموردين المعتمد لمنظومة محجوب أونلاين
    المستخدم في النطاق الجغرافي: (الخوخة، حيس، المخا، عدن)
    """
    __tablename__ = 'suppliers'
    
    # --- المعرفات الأساسية ---
    # المعرف (ID) المولد من واجهة التعميد
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False) # كلمة المرور المؤقتة
    
    # --- البيانات الشخصية والتجارية ---
    owner_name = db.Column(db.String(150), nullable=False) # اسم مالك النشاط
    trade_name = db.Column(db.String(150), nullable=False) # الاسم التجاري للمنشأة
    activity_type = db.Column(db.String(100), nullable=False) # نوع النشاط التجاري
    
    # --- بيانات التوثيق الرسمية ---
    id_type = db.Column(db.String(50), nullable=False) # نوع الهوية (شخصية/جواز/عائلية)
    id_card_number = db.Column(db.String(50), nullable=False) # رقم الهوية المعتمد
    
    # --- الجغرافيا وقنوات الاتصال ---
    phone = db.Column(db.String(20), nullable=False) # رقم التواصل الأساسي
    province = db.Column(db.String(100), nullable=False) # المحافظة
    district = db.Column(db.String(100), nullable=False) # المديرية
    address_detail = db.Column(db.Text, nullable=False) # العنوان التفصيلي (شارع/حي)
    
    # --- الربط المالي (التعميد المالي السيادي) ---
    # رقم المحفظة (e_wallet) المولد من الواجهة لربط المستحقات
    e_wallet = db.Column(db.String(100), unique=True, nullable=False)
    bank_name = db.Column(db.String(100), nullable=False) # اسم البنك أو شركة الصرافة
    bank_acc = db.Column(db.String(100), nullable=False) # رقم الحساب المالي
    
    # --- حالة الحساب السحابي ---
    status = db.Column(db.String(20), default='active') # حالة الحساب (نشط/معلق)
    created_at = db.Column(db.DateTime, default=datetime.utcnow) # تاريخ التعميد

    def __repr__(self):
        return f'<Supplier {self.trade_name} - {self.e_wallet}>'
