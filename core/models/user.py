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

    # التعديل السيادي: نستخدم اسم 'Vendor' كاسم موحد للكلاس لتجنب التضارب
    vendor_profile = db.relationship('Vendor', backref='user', uselist=False, cascade="all, delete-orphan")

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

# --- 2. كلاس المورد (Vendor) ---
# تم تغيير الاسم من Supplier إلى Vendor ليتطابق مع معايير المشروع ويمنع الانهيار
class Vendor(db.Model):
    __tablename__ = 'vendors'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    
    # المعرفات السيادية لمحجوب أونلاين
    supplier_id = db.Column(db.String(50), unique=True) # المعرف مثل MAH-963
    trade_name = db.Column(db.String(150))
    owner_name = db.Column(db.String(150))
    phone = db.Column(db.String(20))
    e_wallet = db.Column(db.String(100), unique=True)
    
    activity_type = db.Column(db.String(100))
    province = db.Column(db.String(100))
    district = db.Column(db.String(100))
    
    # الأرصدة السيادية الثلاثة
    balance_yer = db.Column(db.Float, default=0.0)
    balance_sar = db.Column(db.Float, default=0.0)
    balance_usd = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f"<Vendor {self.trade_name} - ID: {self.supplier_id}>"

# --- 3. إدارة طلبات السحب المالية ---
class WithdrawRequest(db.Model):
    __tablename__ = 'withdraw_requests'
    id = db.Column(db.Integer, primary_key=True)
    # ربط الطلب بجدول الموردين (vendors)
    vendor_id = db.Column(db.Integer, db.ForeignKey('vendors.id'))
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='YER')
    status = db.Column(db.String(20), default='pending')
