# coding: utf-8
# 📂 apps/models/statement_db.py

import os
from apps.extensions import db
from apps.utils.security import AESCipher

# تهيئة مشفر البيانات مع التحقق من المفتاح السيادي
encryption_key = os.getenv('ENCRYPTION_KEY')
if not encryption_key:
    print("⚠️ تحذير أمني: ENCRYPTION_KEY غير موجود في سجل الحسابات! تم تفعيل المفتاح الاحتياطي.")
    encryption_key = '00000000000000000000000000000000'

cipher = AESCipher(encryption_key)

class SupplierStatement(db.Model):
    """
    نموذج القيود والعمليات المحاسبية للموردين - محصن ومشفر ومفهرس للأداء العالي
    """
    __tablename__ = 'supplier_statements'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # ⚡ تم إضافة index=True لمنع عمليات الـ Full Table Scan وتسريع جلب كشوفات الحساب فوراً
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False, index=True)
    
    # الاعتماد على توقيت خادم قاعدة البيانات لتجنب تضارب التوقيت العالمي للمنصة
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=False)
    
    # حقول التخزين المشفر للقيم الحساسة (Ciphertext)
    _description = db.Column(db.String(500), nullable=True) 
    _debit = db.Column(db.String(255), default=lambda: cipher.encrypt("0.0"), nullable=False)
    _credit = db.Column(db.String(255), default=lambda: cipher.encrypt("0.0"), nullable=False)
    _running_balance = db.Column(db.String(255), nullable=False)
    
    currency = db.Column(db.String(10), default='USD', nullable=False)

    # --- بوابات التشفير وفك التشفير الآمنة (Properties) ---

    @property
    def description(self): 
        try:
            return cipher.decrypt(self._description) if self._description else ""
        except Exception:
            return ""
    @description.setter
    def description(self, value): 
        self._description = cipher.encrypt(str(value)) if value else None

    @property
    def debit(self): 
        try:
            return float(cipher.decrypt(self._debit))
        except Exception:
            return 0.0
    @debit.setter
    def debit(self, value): 
        self._debit = cipher.encrypt(str(float(value or 0.0)))

    @property
    def credit(self): 
        try:
            return float(cipher.decrypt(self._credit))
        except Exception:
            return 0.0
    @credit.setter
    def credit(self, value): 
        self._credit = cipher.encrypt(str(float(value or 0.0)))

    @property
    def running_balance(self): 
        try:
            return float(cipher.decrypt(self._running_balance))
        except Exception:
            return 0.0
    @running_balance.setter
    def running_balance(self, value): 
        self._running_balance = cipher.encrypt(str(float(value or 0.0)))

    def __repr__(self):
        return f'<SupplierStatement {self.id} - Supplier ID: {self.supplier_id}>'
