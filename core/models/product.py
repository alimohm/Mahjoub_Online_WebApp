from core import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'product'
    id = db.Column(db.Integer, primary_key=True)
    
    # --- 🔗 جسر الربط مع "قمرة" ---
    # هذا هو الـ ID الخاص بالمنتج في منصة قمرة (ضروري لعمل الـ GraphQL)
    q_product_id = db.Column(db.String(100), unique=True, nullable=True) 
    
    # نكتفي بالاسم فقط للعرض السريع في لوحة المورد
    name = db.Column(db.String(200), nullable=False)
    
    # --- 💰 الترسانة المالية (متعددة العملات) ---
    cost_price = db.Column(db.Float, nullable=False, default=0.0) # تكلفة المورد (الصافي)
    currency = db.Column(db.String(10), default='SAR') # العملة: SAR, USD, YER
    
    # سعر البيع النهائي في متجر قمرة (للمقارنة وحساب هامش ربح المنصة)
    sale_price = db.Column(db.Float, nullable=True) 
    
    # --- 📊 الحالة والحوكمة ---
    # pending (بانتظار المراجعة), active (منشور في قمرة), rejected (مرفوض)
    status = db.Column(db.String(50), default='pending') 
    
    # هل البيانات مطابقة حالياً لما هو موجود في قمرة؟
    is_synced = db.Column(db.Boolean, default=False) 
    
    # --- 🤝 الارتباط السيادي ---
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # إضافة علاقة للوصول لبيانات المورد بسهولة
    supplier = db.relationship('Supplier', backref=db.backref('products', lazy=True))

    def __repr__(self):
        return f'<Product: {self.name} | QID: {self.q_product_id} | Supplier: {self.supplier_id}>'
