# core/models/__init__.py
from core import db

# استيراد الموديل لضمان تسجيله في SQL Alchemy
from core.models.user import User

# بمجرد أن تجهز ملفات الموردين والطلبات، قم بإلغاء التعليق:
# from core.models.supplier import Supplier
# from core.models.order import Order

# تعريف الحزم المصدرة
__all__ = ['User']

# استيراد النماذج من الملفات المنفصلة لجعلها مرئية لـ Django
from .vendor import Vendor

# إذا كان لديك نماذج أخرى مستقبلاً، يتم إضافتها هنا بنفس الطريقة
# from .customer import Customer
# from .product import Product

__all__ = ['Vendor']
