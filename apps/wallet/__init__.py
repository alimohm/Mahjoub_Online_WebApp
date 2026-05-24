# -*- coding: utf-8 -*-
"""
📂 apps/wallet/__init__.py
ملف تهيئة حزمة إدارة المحافظ والتسويات المادية الشاملة
منصة محجوب أونلاين - سوقك الذكي (2026)
"""

# استدعاء الـ Blueprint المحدث ومحرك التسويات من الملف الحوكمي الجديد
from apps.wallet.approvals_and_settlements import wallet_blueprint
# استدعاء النماذج لضمان تسجيل الجداول (الأب والابن) ضمن سياق قاعدة البيانات
from apps.wallet import models

# جعل الـ Blueprint متاحاً بشكل مباشر عند استدعاء الحزمة من التطبيق الرئيسي
__all__ = ['wallet_blueprint']
