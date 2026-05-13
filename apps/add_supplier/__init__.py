# استيراد الـ Blueprint من ملف الروابط المحلي
from .routes import admin_suppliers

# تصدير الـ Blueprint ليكون متاحاً عند استدعائه في create_app
__all__ = ['admin_suppliers']
