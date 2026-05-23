# coding: utf-8
# تجميع وإشهار النماذج لسهولة الاستيراد من خارج حزمة models

from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier  # استدعاء الموردين من ملفها المستقل والصحيح ✅

# أي موديلات جديدة تقوم بإنشائها مستقبلاً في ملفات أخرى، قم بإشهارها هنا كالتالي:
# from apps.models.products import Product
