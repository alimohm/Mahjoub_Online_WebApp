# core/models/__init__.py

from core import db

# 1. استيراد نماذج الهوية والمستخدمين
from core.models.user import User

# 2. استيراد نماذج الأعمال والربط السيادي (المحافظات، المديريات، الموردين)
from .business import Province, District, FinancialEntity, Supplier, Order

# 3. استيراد نماذج المتاجر والمنتجات
from .vendor import Vendor
from .product import Product

# استيراد طلبات السحب إذا كانت موجودة في ملف vendor
try:
    from .vendor import WithdrawRequest
except ImportError:
    WithdrawRequest = None

# 4. تعريف الحزم المصدرة (قائمة واحدة شاملة لضمان رؤية النظام لكل الجداول)
__all__ = [
    'db',
    'User',
    'Province',
    'District',
    'FinancialEntity',
    'Supplier',
    'Order',
    'Vendor',
    'Product',
    'WithdrawRequest'
]
