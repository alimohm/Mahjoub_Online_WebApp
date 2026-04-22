import os

class Config:
    # مفتاح الأمان الأساسي لتشفير الجلسات (Sessions)
    SECRET_KEY = os.environ.get('SECRET_KEY', 'mahjoub_safe_key_2026')
    
    # جلب رابط قاعدة البيانات من إعدادات Railway
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # إيقاف تنبيهات التعديل لتوفير موارد السيرفر
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات الربط مع منصة قمرة (سوقك الذكي)
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')

    # لضمان ظهور النصوص العربية بشكل صحيح في النظام
    JSON_AS_ASCII = False
