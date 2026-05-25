# coding: utf-8
# 🔑 مستند النموذج الحوكمي للموردين - منصة محجوب أونلاين 2026

import random
from apps.extensions import db
from datetime import datetime
from sqlalchemy.orm import validates

# حذفنا سطر الاستيراد المباشر لـ SupplierStatement لتجنب Circular Import

class Supplier(db.Model):
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    sovereign_id = db.Column(db.String(50), unique=True, nullable=False, index=True) 
    wallet_code = db.Column(db.String(50), unique=True, nullable=False)
    
    # ربط العلاقة مع كشوفات الحسابات باستخدام اسم الموديل كسلسلة نصية
    statements = db.relationship('SupplierStatement', backref='supplier', lazy='dynamic')

    # ... (بقية الحقول كما هي دون تغيير)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    identity_type = db.Column(db.String(50), nullable=False)   
    identity_number = db.Column(db.String(50), unique=True, nullable=False)  
    identity_image = db.Column(db.String(255))   
    owner_name = db.Column(db.String(150), unique=True, nullable=False)
    owner_phone = db.Column(db.String(20), unique=True, nullable=False)        
    trade_name = db.Column(db.String(150), unique=True, nullable=False)
    shop_phone = db.Column(db.String(20), unique=True, nullable=False)
    activity_type = db.Column(db.String(50))      
    province = db.Column(db.String(50))
    district = db.Column(db.String(50))
    address_detail = db.Column(db.Text) 
    fin_type = db.Column(db.String(20))          
    bank_name = db.Column(db.String(100))        
    bank_acc = db.Column(db.String(50), unique=True, nullable=False)          
    status = db.Column(db.String(20), nullable=False, default='pending') 
    rank_grade = db.Column(db.String(20), nullable=False, default='ريادي') 
    registration_source = db.Column(db.String(30), nullable=False, default='الموقع الخارجي') 
    created_by_id = db.Column(db.Integer, nullable=True)  
    updated_by_id = db.Column(db.Integer, nullable=True)  
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow) 
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow) 

    # 📊 خاصية الرصيد
    @property
    def balance(self):
        # استيراد الموديل هنا فقط عند الحاجة لكسر الدائرة
        from apps.models.statement_db import SupplierStatement
        last_stmt = self.statements.order_by(SupplierStatement.created_at.desc()).first()
        return last_stmt.running_balance if last_stmt else 0.0

    # ... (بقية الدوال كما هي)
