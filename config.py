import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'SOVEREIGN_KEY_2026')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') # رابط قاعدة البيانات في Railway
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # نظام الـ Binds لعزل المالية لاحقاً
    # SQLALCHEMY_BINDS = { 'finance': 'رابط_قاعدة_بيانات_المالية' }
