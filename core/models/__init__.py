# core/models/__init__.py

# 1. استيراد قاعدة البيانات من ملف core الأساسي
from core import db

# 2. استيراد الموديل الأساسي (القائد/المستخدم) أولاً
# هذا ضروري لأن الموردين والطلبات تعتمد على وجود جدول 'users'
from .user import User

# 3. استيراد الموديلات التجارية (الموردين، المنتجات، الطلبات)
# تأكد أن ملف business.py يحتوي على تعريف Supplier و Order
from .business import Supplier, Order

# 4. (اختياري) تعريف القائمة لسهولة الاستخدام عند الاستيراد الخارجي
__all__ = ['User', 'Supplier', 'Order']
