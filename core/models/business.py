from core import db
from datetime import datetime

# ============================================================
# جداول البنية التحتية الجغرافية (Geographic Infrastructure)
# ============================================================

class Province(db.Model):
    """
    موديل المحافظات: لتصنيف النطاق الجغرافي للترسانة (عدن، الحديدة، إلخ)
    """
    __tablename__ = 'provinces'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    
    # علاقة لجلب كافة المديريات التابعة لهذه المحافظة
    districts = db.relationship('District', backref='province', lazy=True)

    def __repr__(self):
        return f"<Province {self.name}>"

class District(db.Model):
    """
    موديل المديريات: يمثل نقاط التمركز الدقيقة (الخوخة، حيس، المخاء، إلخ)
    """
    __tablename__ = 'districts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'), nullable=False)

    def __repr__(self):
        return f"<District {self.name}>"

# ============================================================
# جداول الربط المالي (Financial Connectivity)
# ============================================================

class FinancialEntity(db.Model):
    """
    موديل الجهات المالية: البنوك الإسلامية وشركات الصرافة المعتمدة
    """
    __tablename__ = 'financial_entities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False) # بنك الكريمي، القطيبي، إلخ
    entity_type = db.Column(db.String(50))           # 'bank' أو 'exchange'
    active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<FinancialEntity {self.name}>"

# ============================================================
# جداول النشاط التجاري (Core Business Models)
# ============================================================

class Supplier(db.Model):
    """
    موديل الموردين المطور: يربط شركاء الترسانة بالهوية الرقمية والجغرافية
    """
    __tablename__ = 'suppliers'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    trade_name = db.Column(db.String(150)) # الاسم التجاري (سوقك الذكي)
    
    # الروابط الجغرافية الديناميكية
    province_id = db.Column(db.Integer, db.ForeignKey('provinces.id'))
    district_id = db.Column(db.Integer, db.ForeignKey('districts.id'))
    address_detail = db.Column(db.Text) # العنوان التفصيلي
    
    phone = db.Column(db.String(20), nullable=True)
    
    # بيانات الهوية والأرشفة
    id_card_number = db.Column(db.String(50))
    id_image = db.Column(db.String(255)) # مسار صورة الهوية
    
    # الربط المالي السيادي
    e_wallet = db.Column(db.String(100), unique=True) # رمز المحفظة
    bank_id = db.Column(db.Integer, db.ForeignKey('financial_entities.id'))
    bank_acc = db.Column(db.String(100))
    
    # ربط المورد بحساب القائد (User)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # علاقة الطلبات
    orders = db.relationship('Order', backref='supplier', lazy=True)

    def __repr__(self):
        return f"<Supplier {self.name} - Wallet: {self.e_wallet}>"

class Order(db.Model):
    """
    موديل الطلبات: لتتبع حركة السلع والسيولة المركزية
    """
    __tablename__ = 'orders'
    
    id = db.Column(db.Integer, primary_key=True)
    amount = db.Column(db.Float, nullable=False, default=0.0)
    status = db.Column(db.String(50), default='قيد التدقيق')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), nullable=False)

    def __repr__(self):
        return f"<Order {self.id} - {self.status}>"
