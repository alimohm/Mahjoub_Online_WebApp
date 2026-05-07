# config.py
import os

class Config:
    """
    إعدادات الترسانة السيادية لمنصة محجوب أونلاين.
    تم ضبط هذا الملف ليتوافق مع بيئة Railway السحابية.
    """

    # --- 1. إعدادات قاعدة البيانات (Database Configuration) ---
    # الأولوية دائماً لمتغير DATABASE_URL الذي يوفره Railway تلقائياً
    uri = os.environ.get('DATABASE_URL')
    
    # في حال عدم وجود DATABASE_URL (أو عند العمل محلياً)، نستخدم رابط Railway التفصيلي
    # لاحظ استخدام f-string لدمج المتغيرات البرمجية داخل الرابط
    if not uri:
        # الربط السيادي المعتمد لبيئة Railway
        uri = f"postgresql://{os.environ.get('PGUSER', 'postgres')}:{os.environ.get('POSTGRES_PASSWORD')}@{os.environ.get('RAILWAY_PRIVATE_DOMAIN', 'localhost')}:5432/{os.environ.get('PGDATABASE', 'railway')}"
    
    # معالجة اختلاف تسمية البروتوكول لضمان توافق SQLAlchemy
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # --- 2. إعدادات الأمان والسيادة ---
    # سر الأمان السيادي لـ محجوب أونلاين - يفضل دائماً وضعه في Environment Variables
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ali_Mahjoub_High_Energy_2026_Resonance'

    # --- 3. إعدادات الأرشفة والاتصال بـ GitHub (Sovereign Assets) ---
    # سحب التوكن والمستودع من متغيرات البيئة لضمان الخصوصية
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') 
    GITHUB_REPO = os.environ.get('GITHUB_REPO')
    
    # قيم احتياطية (Fallback) لضمان عدم توقف النظام أثناء التطوير
    if not GITHUB_TOKEN:
        GITHUB_TOKEN = "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"
    
    if not GITHUB_REPO:
        GITHUB_REPO = "alimohm/Mahjoub-Sovereign-Assets"
    
    # مسار المجلد الرئيسي للأرشفة الرقمية للترسانة
    GITHUB_MAIN_PATH = "Main_Archive"

    # --- 4. إعدادات الأداء والإنتاج (Production Stability) ---
    # لضمان استقرار الاتصال ومنع حدوث المهلة الزمنية (Timeout) في Railway
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,  # التحقق من سلامة الاتصال قبل كل استعلام
        "pool_recycle": 280,    # إعادة تدوير الاتصالات قبل انتهاء مهلة السيرفر
        "pool_size": 10,        # عدد الاتصالات المفتوحة المتزامنة
        "max_overflow": 20,     # أقصى عدد اتصالات إضافية عند الضغط العالي
    }

    # رسالة تشغيل داخلية (يمكن إلغاؤها في الإنتاج)
    # print(f"🚀 Sovereign Database URI Initialized Successfully.")
