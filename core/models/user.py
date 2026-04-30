from core import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    """
    موديل المستخدمين - النواة السيادية للهوية الرقمية في منصة محجوب أونلاين.
    يدعم الأسماء بالعربية وتعدد الأدوار (قائد، مورد، عميل).
    """
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # اسم المستخدم: تم رفع الطول لـ 150 لدعم الأسماء العربية المركبة بسلاسة
    username = db.Column(db.String(150), unique=True, nullable=False)
    
    # البريد الإلكتروني للارتباط الرسمي وتوثيق الحساب
    email = db.Column(db.String(120), unique=True, nullable=False)
    
    # تخزين مفتاح التشفير بدلاً من كلمة المرور الصريحة لتعزيز الأمان
    password_hash = db.Column(db.String(255), nullable=False)
    
    # حوكمة الأدوار: 
    # 'admin' -> القائد علي محجوب (تحكم كامل)
    # 'supplier' -> شركاء الترسانة (إدارة منتجاتهم)
    # 'user' -> العملاء والمتسوقين
    role = db.Column(db.String(20), nullable=False, default='supplier')
    
    # حالة الحساب السيادية: تتيح للقائد إيقاف أو تفعيل أي حساب في المنصة
    is_active_account = db.Column(db.Boolean, default=True)
    
    # تاريخ الانضمام للمنصة
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def set_password(self, password):
        """
        تحويل كلمة المرور النصية إلى هاش مشفر غير قابل للكسر.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        التحقق من مطابقة كلمة المرور المدخلة مع الهاش المخزن عند الولوج.
        """
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        """
        التمثيل النصي للكائن داخل بيئة التطوير (برج الرقابة).
        """
        return f'<User {self.username} - Role: {self.role} - Status: {"Active" if self.is_active_account else "Blocked"}>'
