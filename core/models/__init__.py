# core/models/__init__.py
from core import db

# 1. استيراد النماذج الأساسية
from .user import User
from .vendor import Vendor, WithdrawRequest

# 2. استيراد النماذج اللوجستية (مع معالجة أخطاء الاستيراد)
try:
    from .product import Product
except ImportError:
    Product = None

try:
    from .business import Order
except ImportError:
    Order = None

# 3. قائمة التصدير الموحدة (تم حذف Supplier نهائياً)
__all__ = [
    'db',
    'User',
    'Vendor',
    'WithdrawRequest',
    'Product',
    'Order'
]
