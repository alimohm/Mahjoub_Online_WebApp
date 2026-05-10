# config.py
import os

class Config:
    """
    إعدادات الترسانة السيادية لمنصة محجوب أونلاين v4.0.
    تم التحسين لدعم الأرشفة التلقائية، أسعار الصرف، وحماية Railway.
    """

    # --- 1. إعدادات قاعدة البيانات (Database Configuration) ---
    uri = os.environ.get('DATABASE_URL')
    
    if not uri:
        # الربط السيادي الاحتياطي لبيئة Railway
        user = os.environ.get('PGUSER', 'postgres')
        password = os.environ.get('POSTGRES_PASSWORD')
        host = os.environ.get('RAILWAY_PRIVATE_DOMAIN', 'localhost')
        db_name = os.environ.get('PGDATABASE', 'railway')
        uri = f"postgresql://{user}:{password}@{host}:5432/{db_name}"
    
    # تصحيح البروتوكول لـ SQLAlchemy
    if uri and uri.startswith("postgres://"):
        uri = uri.replace("postgres://", "postgresql://", 1)
        
    SQLALCHEMY_DATABASE_URI = uri
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # خيارات الأداء العالي (Production Stability)
    SQLALCHEMY_ENGINE_OPTIONS = {
        "pool_pre_ping": True,
        "pool_recycle": 280,
        "pool_size": 15,
        "max_overflow": 25,
    }

    # --- 2. إعدادات الأمان والسيادة ---
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'Ali_Mahjoub_High_Energy_2026_Resonance'

    # --- 3. إعدادات الأرشفة و GitHub (Sovereign Assets) ---
    # دمج التوكن الذي أرسلته سابقاً كخيار افتراضي (Fallback)
    GITHUB_TOKEN = os.environ.get('GITHUB_TOKEN') or "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"
    GITHUB_REPO = os.environ.get('GITHUB_REPO') or "Ali-Mahjoub/Mahjoub-Online-Archive"
    GITHUB_MAIN_PATH = "Main_Archive"

    # --- 4. إعدادات محرك العملات والعمولات ---
    DEFAULT_SAR_RATE = 530.0
    DEFAULT_USD_RATE = 1600.0
    PLATFORM_MARKUP = 0.10  # عمولة محجوب أونلاين (10%)

    # --- 5. مسارات الملفات الثابتة ---
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # الحد الأقصى لحجم الصور (16 ميجا)
