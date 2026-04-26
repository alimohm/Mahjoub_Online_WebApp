import os
from dotenv import load_dotenv

# تحميل ملف .env للعمل محلياً
load_dotenv()

class Config:
    # 1. إعدادات قاعدة البيانات
    database_url = os.environ.get('DATABASE_URL')
    
    if database_url:
        # تصحيح البروتوكول ليتوافق مع SQLAlchemy الحديثة
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        
        # إضافة sslmode=require للاتصال الآمن بالسحابة (Railway/Render)
        if "sslmode=" not in database_url:
            separator = "&" if "?" in database_url else "?"
            database_url += f"{separator}sslmode=require"
                
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 2. إعدادات "قمرة" (Qumra) المستدعاة في qumra_handler
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')
    
    # 3. حماية الجلسات والبيانات السيادية
    SECRET_KEY = os.environ.get('SECRET_KEY', 'MAHJOUB_ONLINE_SECURE_2026')
    
    # إعدادات إضافية لاستقرار تسجيل الدخول
    SESSION_COOKIE_SECURE = True  # تشغيل الكوكي عبر HTTPS فقط
    REMEMBER_COOKIE_DURATION = 3600 * 24 * 7 # تذكر الدخول لمدة أسبوع
