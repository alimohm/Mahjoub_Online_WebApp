from core import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import InternalError, ProgrammingError

# --- 1. كلاس المستخدم (الرقابة والهوية) ---
class User(db.Model, UserMixin):
    __tablename__ = 'users' 

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(50), default='admin') 
    is_active_account = db.Column(db.Boolean, default=True)

    # الربط السيادي: يشير إلى كلاس 'Supplier' المعرف أدناه
    supplier = db.relationship('Supplier', backref='user', uselist=False, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        if not self.password_hash: return False
        return check_password_hash(self.password_hash, password)

    @property
    def is_active(self):
        try:
            return self.is_active_account
        except (InternalError, ProgrammingError, Exception):
            db.session.rollback()
            return True 

    def get_id(self):
        return str(self.id)

# --- 2. كلاس المورد (الترسانة والعمليات) ---
# ملاحظة: هذا الكلاس يحل مشكلة الانهيار لأنه يوفر المفتاح الأجنبي المطلوب
class Supplier(db.Model):
    __tablename__ = 'vendors' # الحفاظ على اسم الجدول الحالي في القاعدة

    id = db.Column(db.Integer, primary_key=True)
    
    # القيد الجوهري: ربط المورد بحساب المستخدم عبر ForeignKey
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # المعرفات السيادية لمحجوب أونلاين
    supplier_id = db.Column(db.String(50), unique=True) # مثال: MAH-963
    trade_name = db.Column(db.String(150)) # الاسم التجاري
    owner_name = db.Column(db.String(150)) # اسم المالك
    phone = db.Column(db.String(20))
    e_wallet = db.Column(db.String(100), unique=True) # المحفظة السيادية
    
    # بيانات النشاط والموقع
    activity_type = db.Column(db.String(100))
    province = db.Column(db.String(100)) # المحافظة
    district = db.Column(db.String(100)) # المديرية
    
    # الهندسة المالية (الأرصدة)
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Supplier {self.trade_name} - ID: {self.supplier_id}>"

# --- 3. إدارة طلبات السحب المالية ---
class WithdrawRequest(db.Model):
    __tablename__ = 'withdraw_requests'
    id = db.Column(db.Integer, primary_key=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='YER')
    status = db.Column(db.String(20), default='pending') # pending, approved, rejected
