# استيراد الموديلات لضمان تسجيلها في محرك SQLAlchemy السيادي
# هذا الترتيب يضمن بناء العلاقات (Foreign Keys) بدون أخطاء

try:
    from .user import User
    from .supplier import Supplier
    from .product import Product
    
    # رسالة تأكيد تظهر في سجلات Railway للتأكد من التحميل
    print("✅ [Models] تم تسجيل جميع الموديلات (User, Supplier, Product) في النظام بنجاح.")
except ImportError as e:
    print(f"⚠️ [Critical] فشل في استيراد الموديلات: {e}")

# تصدير الموديلات لتسهيل استدعائها من أي مكان في المشروع
__all__ = ['User', 'Supplier', 'Product']
