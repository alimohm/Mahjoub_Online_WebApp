from core.models.user import User
from core.models.product import Product
from core.models.supplier import Supplier

# هذا السطر يسهل عملية استدعاء db.create_all() من ملف النواة الرئيسي
__all__ = ['User', 'Product', 'Supplier']
