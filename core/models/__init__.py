from core import db

# 1. استيراد الهوية السيادية من الملف الموحد (user.py)
# تم تحديث المسار ليكون الاستيراد من .user لإنهاء خطأ ModuleNotFoundError نهائياً
from .user import User, Vendor, WithdrawRequest

# 2. استيراد المكونات الإضافية (المنتجات والعمليات) مع الحماية من الانهيار
try:
    from .product import Product
except ImportError:
    Product = None

try:
    from .business import Order
except ImportError:
    Order = None

# 3. تعريف المكونات المتاحة للنظام (تصدير الوحدات السيادية)
# هذا السطر يضمن أن النظام يرى الموردين وطلبات السحب كجزء أساسي من نماذج البيانات
__all__ = ['db', 'User', 'Vendor', 'WithdrawRequest', 'Product', 'Order']
