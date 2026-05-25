# coding: utf-8
# 📂 apps/models/statement_db.py
from apps.extensions import db
from datetime import datetime

class SupplierStatement(db.Model):
    __tablename__ = 'supplier_statements'
    
    id = db.Column(db.Integer, primary_key=True)
    # الربط يتم برمجياً بدون استيراد كلاس المورد
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)
    
    amount = db.Column(db.Float, nullable=False)
    running_balance = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='USD')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
