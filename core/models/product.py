from core import db
from datetime import datetime

class Product(db.Model):
    """
    نموذج المنتج السيادي: يعمل كجسر ربط بين نظام محجوب أونلاين ومنصة قمرة.
    يتم تخزين البيانات المالية والروابط التقنية فقط، بينما تبقى الأصول (الصور والوصف) في السحابة.
    """
    __tablename__ = 'product'
    
    # المعرف المحلي الفريد في قاعدة بياناتنا (Render)
    id = db.Column(db.Integer, primary_key=True)
    
    # --- 🔗 جسر الربط التقني مع "قمرة" ---
    # معرف المنتج في قمرة (نحصل عليه عبر GraphQL) لاستدعاء البيانات لحظياً
    q_product_id = db.Column(db.String(100), unique=True, nullable=True) 
    
    # اسم المنتج للعرض السريع في لوحة المورد والإدارة
    name = db.Column(db.String(200), nullable=False)
    
    # --- 💰 الترسانة المالية (نظام حماية العملات) ---
    # سعر التكلفة الذي حدده المورد (الصافي)
    cost_price = db.Column(db.Float, nullable=False, default=0.0) 
    
    # العملة المعتمدة للمنتج لضمان استقرار الأرباح (SAR, USD, YER)
    currency = db.Column(db.String(10), default='SAR') 
    
    # سعر البيع النهائي المعروض للزبائن في متجر قمرة (للمقارنة والمراقبة)
    sale_price = db.Column(db.Float, nullable=True) 
    
    # --- 📊 مصفوفة الحالة والحوكمة ---
    # الحالات: pending (تحت المراجعة), active (منشور), rejected (مرفوض)
    status = db.Column(db.String(50), default='pending') 
    
    # مؤشر تقني للتأكد من نجاح مزامنة السعر والبيانات مع قمرة
    is_synced = db.Column(db.Boolean, default=False) 
    
    # --- 🤝 الارتباط السيادي (هوية المورد) ---
    # الربط بالمورد صاحب المنتج لضمان توجيه الأرباح والطلبات له
    supplier_id = db.Column(db.Integer, db.ForeignKey('supplier.id'), nullable=False)
    
    # تاريخ إضافة المنتج للترسانة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # ملاحظة سيادية: 
    # تم حذف سطر db.relationship هنا لتجنب خطأ التعارض الذي ظهر في الـ Logs.
    # العلاقة يتم إدارتها الآن من جهة نموذج Supplier عبر backref='products'.

    def __repr__(self):
        return f'<Product: {self.name} | QID: {self.q_product_id} | SupplierID: {self.supplier_id}>'
