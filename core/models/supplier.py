# core/models/supplier.py
import os
import json
import base64
import requests
from datetime import datetime
from core import db

class Supplier(db.Model):
    """
    موديل المورد السيادي - قاعدة البيانات المركزية لترسانة محجوب أونلاين
    تم التحديث ليتوافق مع واجهة التعميد الملكية (البنوك، الهوية، النطاق الجغرافي)
    """
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True) # مثال: SUP_101#
    trade_name = db.Column(db.String(150), nullable=False) # الاسم التجاري
    owner_name = db.Column(db.String(150)) # اسم المالك الرباعي
    
    # بيانات الهوية والنشاط (جديد لتوافق الواجهة)
    activity_type = db.Column(db.String(100)) # تصنيف النشاط
    identity_type = db.Column(db.String(50)) # نوع الهوية
    identity_image = db.Column(db.String(255)) # مسار صورة الهوية في السيرفر
    
    # النطاق الجغرافي (العنوان)
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    address_detail = db.Column(db.Text) # العنوان التفصيلي (أقرب معلم)
    
    phone = db.Column(db.String(20)) # رقم الواتساب
    tier = db.Column(db.String(50), default='مبتدئ') # (سيادي، ذهبي، مبتدئ)
    
    # الربط المالي (بيانات الحساب البنكي)
    bank_name = db.Column(db.String(150)) # اسم البنك أو الصراف
    bank_acc = db.Column(db.String(100)) # رقم الحساب أو الآيبان
    
    # سجلات الأرصدة المتعددة (المحفظة الثلاثية)
    balance_yer = db.Column(db.Float, default=0.0) # يمني
    balance_sar = db.Column(db.Float, default=0.0) # سعودي
    balance_usd = db.Column(db.Float, default=0.0) # دولار
    
    status = db.Column(db.String(20), default='active') 
    staff_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """تحويل البيانات إلى JSON لتغذية لوحة القيادة ونظام الأرشفة"""
        return {
            'id': self.id,
            'sovereign_id': self.sovereign_id or f"SUP_{self.id}#",
            'trade_name': self.trade_name,
            'owner_name': self.owner_name,
            'activity_type': self.activity_type,
            'identity_type': self.identity_type,
            'province': self.province,
            'district': self.district,
            'address_detail': self.address_detail,
            'phone': self.phone,
            'bank_name': self.bank_name,
            'bank_acc': self.bank_acc,
            'tier': self.tier,
            'balance_yer': self.balance_yer,
            'balance_sar': self.balance_sar,
            'balance_usd': self.balance_usd,
            'status': self.status,
            'staff_count': self.staff_count,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

class SupplierStaff(db.Model):
    """ موديل طاقم الموردين - يتبع نافذة الموردين """
    __tablename__ = 'supplier_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100)) # مدير، محاسب، مندوب
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    
    # ربط العلاقة العكسية
    supplier = db.relationship('Supplier', backref=db.backref('staff_members', lazy=True))

class ArchiveManager:
    """ نظام الأرشفة السيادية لتوثيق العمليات على GitHub """
    def __init__(self):
        self.github_token = os.getenv("GITHUB_TOKEN")
        self.repo_name = "Mahjoub_Online_WebApp" # تم التعديل لاسم المستودع الحالي
        self.username = "alimohm" # اسم المستخدم الخاص بك
        self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/contents/"

    def archive_entity(self, entity_obj):
        """ أرشفة بيانات كيان كامل إلى GitHub فوراً كنسخة احتياطية سيادية """
        if not self.github_token: return False
        
        data = entity_obj.to_dict()
        filename = f"Supplier_Archive_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        path = f"core/archives/suppliers/{data['sovereign_id']}/{filename}"
        
        content = json.dumps(data, indent=4, ensure_ascii=False)
        encoded = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        payload = {
            "message": f"🛡️ Sovereign Archive: {data['trade_name']} ({data['sovereign_id']})", 
            "content": encoded
        }
        headers = {
            "Authorization": f"token {self.github_token}", 
            "Accept": "application/vnd.github.v3+json"
        }

        try:
            requests.put(self.base_url + path, headers=headers, json=payload, timeout=10)
            return True
        except:
            return False

# تشغيل محرك الأرشفة السيادي
archive_sys = ArchiveManager()
