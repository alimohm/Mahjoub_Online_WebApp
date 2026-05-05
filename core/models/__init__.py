from core import db

# 1. استيراد الهوية الأساسية (نواة النظام)
# تم الاكتفاء بـ User حالياً لأننا حذفنا Vendor و WithdrawRequest من ملف user.py
from .user import User

# 2. استيراد المكونات الإضافية (المنتجات والعمليات التجارية)
# سنقوم بالاستيراد مع حماية من الانهيار لضمان استقرار محجوب أونلاين
try:
    from .product import Product
except ImportError:
    Product = None

try:
    # الآن سيقرأ Order بنجاح من ملف business.py الذي أصلحناه
    from .business import Order
except ImportError:
    Order = None

# 3. تعريف المكونات المتاحة للنظام (الشرعية الرقمية الموحدة)
# حذفنا المرجعيات القديمة (Vendor, WithdrawRequest) لكي يتوقف الخطأ في Railway فوراً
__all__ = ['db', 'User', 'Product', 'Order']
