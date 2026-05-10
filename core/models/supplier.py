# core/models/supplier.py

import os
import json
import base64
import requests
from datetime import datetime
from core import db  # استيراد كائن قاعدة البيانات المركزي

class Supplier(db.Model):
    """
    موديل المورد السيادي - قاعدة البيانات المركزية لترسانة محجوب أونلاين
    المسؤول عن تخزين بيانات الكيانات التجارية المرتبطة بالنظام
    """
    __tablename__ = 'suppliers'
    
    # المفتاح الأساسي (ضروري جداً لعمل SQLAlchemy)
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True) # المعرف السيادي (مثال: SUP_101#)
    trade_name = db.Column(db.String(150), nullable=False) # اسم المتجر / الكيان
    owner_name = db.Column(db.String(150)) # اسم المالك الرسمي
    province = db.Column(db.String(100)) # المحافظة (الحديدة، صنعاء، عدن...)
    district = db.Column(db.String(100)) # المديرية
    phone = db.Column(db.String(20)) # رقم التواصل
    tier = db.Column(db.String(50), default='مبتدئ') # الرتبة (سيادي، ذهبي، مبتدئ)
    
    # سجلات الأرصدة المتعددة
    balance_yer = db.Column(db.Float, default=0.0) # ريال يمني
    balance_sar = db.Column(db.Float, default=0.0) # ريال سعودي
    balance_usd = db.Column(db.Float, default=0.0) # دولار أمريكي
    
    status = db.Column(db.String(20), default='active') # حالة الحساب (active/suspended)
    staff_count = db.Column(db.Integer, default=0) # عدد الطاقم التابع للمورد
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        """تحويل البيانات إلى JSON لتغذية واجهة الإدارة والبحث اللحظي"""
        return {
            'id': self.id,
            'sovereign_id': self.sovereign_id or f"SUP_{self.id}#",
            'trade_name': self.trade_name,
            'owner_name': self.owner_name,
            'province': self.province,
            'tier': self.tier,
            'balance_yer': self.balance_yer,
            'balance_sar': self.balance_sar,
            'balance_usd': self.balance_usd,
            'status': self.status,
            'staff_count': self.staff_count
        }

class SupplierStaff(db.Model):
    """
    موديل طاقم الموردين - يتبع نافذة الموردين
    """
    __tablename__ = 'supplier_staff'
    
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    name = db.Column(db.String(150), nullable=False)
    role = db.Column(db.String(100)) # مدير، محاسب، مندوب
    phone = db.Column(db.String(20))
    status = db.Column(db.String(20), default='active')
    
    # ربط العلاقة مع المورد
    supplier = db.relationship('Supplier', backref=db.backref('staff_members', lazy=True))

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'role': self.role,
            'phone': self.phone,
            'status': self.status
        }

class ArchiveManager:
    """
    نظام الأرشفة السيادية لترسانة محجوب أونلاين
    المسؤول عن توثيق العمليات ورفعها إلى مستودع GitHub الخاص
    """
    def __init__(self):
        # يفضل وضع التوكن في متغيرات البيئة بـ Railway لاحقاً
        self.github_token = os.getenv("GITHUB_TOKEN", "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")
        self.repo_name = "Mahjoub-Online-Archive" 
        self.username = "Ali-Mahjoub" 
        self.base_url = f"https://api.github.com/repos/{self.username}/{self.repo_name}/contents/"

    def archive_data_as_json(self, data_dict, filename, entity_id, folder_name="Suppliers"):
        """أرشفة البيانات بصيغة JSON ورفعها فوراً إلى GitHub"""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        path = f"Archives/{folder_name}/{entity_id}/{filename}_{timestamp}.json"
        
        content = json.dumps(data_dict, indent=4, ensure_ascii=False)
        encoded_content = base64.b64encode(content.encode('utf-8')).decode('utf-8')

        payload = {
            "message": f"Sovereign Archive: {filename} for {entity_id}",
            "content": encoded_content
        }

        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.put(self.base_url + path, headers=headers, json=payload)
        return response.status_code in [201, 200]

# إنشاء نسخة مفعلة وجاهزة للاستخدام في النظام
archive_sys = ArchiveManager()
