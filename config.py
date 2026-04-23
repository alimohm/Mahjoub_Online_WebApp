import os
from dotenv import load_dotenv

# تحميل الإعدادات من ملف .env
load_dotenv()

class Config:
    # سرية الجلسات والتشفير
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'mahjoub_online_default_key_2026'
    
    # إعدادات قاعدة البيانات (PostgreSQL)
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # إعدادات منصة قمرة (GraphQL)
    QUMRA_API_KEY = os.environ.get('QUMRA_API_KEY')
    QUMRA_API_URL = os.environ.get('QUMRA_API_URL')
    
    # إعدادات المجلدات المؤقتة (ترانزيت الصور)
    UPLOAD_FOLDER = os.path.join('static', 'img', 'temp_uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # حد أقصى 16 ميجا للرفع

    # إعدادات الأرشفة الخارجية (روابط ثابتة)
    EXTERNAL_ARCHIVE_URL = "https://archive.mahjoub.online/v1/upload"
