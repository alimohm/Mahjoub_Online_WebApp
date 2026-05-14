# coding: utf-8
# - نقطة انطلاق التطبيق
import os
from flask import Flask
# 💡 استيراد آمن من مجلد models
from models.admin_db import db, AdminUser 

def create_app():
    """
    دالة بناء التطبيق (App Factory):
    تقوم بتجميع الإعدادات وربط قاعدة البيانات.
    """
    app = Flask(__name__)
    
    # إعدادات الاتصال بقاعدة البيانات (PostgreSQL في Railway)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'default_key_2026')
    
    # ربط القاعدة بالتطبيق
    db.init_app(app)
    
    with app.app_context():
        # إنشاء الجداول تلقائياً عند أول تشغيل
        db.create_all()
        
    return app

# 🚀 المتغير الذي يحتاجه gunicorn للتشغيل
app = create_app()

if __name__ == "__main__":
    # التشغيل المحلي
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
