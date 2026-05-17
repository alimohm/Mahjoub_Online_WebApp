# config.py
# coding: utf-8
# ⚙️ مهندس الإعدادات المركزية - منصة محجوب أونلاين 2026

import os

class Config:
    # مفتاح الأمان السيادي للمنصة
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SOVEREIGN_KEY_2026')
    
    # 1. جلب رابط قاعدة البيانات من بيئة Railway السحابية
    db_url = os.environ.get('DATABASE_URL')
    
    # 2. 🛡️ التعديل الجوهري: معالجة وإصلاح بادئة الرابط ليتوافق مع SQLAlchemy الحديثة
    if db_url and db_url.startswith("postgres://"):
        db_url = db_url.replace("postgres://", "postgresql://", 1)
        
    # 3. إسناد الرابط المصحح، أو استخدام قاعدة بيانات SQLite محلية كخط دفاع احتياطي لمنع الانهيار
    SQLALCHEMY_DATABASE_URI = db_url or 'sqlite:///mahjoub_fallback.db'
    
    # إيقاف تتبع التعديلات لرفع أداء السيرفر وتوفير موارد الاستضافة
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # نظام الـ Binds لعزل الحسابات والمالية لاحقاً (مجهز للمستقبل)
    # SQLALCHEMY_BINDS = { 'finance': 'رابط_قاعدة_بيانات_المالية' }
