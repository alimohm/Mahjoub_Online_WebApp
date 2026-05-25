# coding: utf-8
# 📂 apps/models/__init__.py
# تجميع وإشهار النماذج لسهولة الاستيراد من خارج حزمة models

from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier

# استيراد موديلات المحفظة وإشهارها باسم 'Wallet' لتتوافق مع طلبات الاستيراد في routes.py
# تأكد أن اسم الكلاس داخل ملف wallet_db.py هو بالفعل SupplierWallet
from apps.models.wallet_db import SupplierWallet as Wallet, WalletTransaction

# إشهار موديل التسويات الإدارية
from apps.models.settlements_db import AdminSettlement

# هذا الملف الآن يضمن أن أي ملف (مثل routes.py) عند كتابته:
# from apps.models import Wallet
# سيجد الكلاس الصحيح دون أي أخطاء.
