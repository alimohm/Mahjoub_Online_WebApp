# coding: utf-8
# 📂 apps/models/__init__.py - مجمع النماذج المحدث

from .admin_db import AdminUser
from .supplier_db import Supplier
from .wallet_db import SupplierWallet, WalletTransaction
from .vault_db import AdminVault, VaultTransaction
from .financial_db import ExchangeRate, FinancialLog
from .bridge_db import Product, ProductVariant  # <--- إضافة النماذج الجديدة هنا

__all__ = [
    'AdminUser', 
    'Supplier', 
    'SupplierWallet', 
    'WalletTransaction', 
    'AdminVault', 
    'VaultTransaction',
    'ExchangeRate',
    'FinancialLog',
    'Product',        # <--- إضافة النماذج الجديدة هنا
    'ProductVariant'  # <--- إضافة النماذج الجديدة هنا
]
