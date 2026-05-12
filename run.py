import os
from flask import Flask
from core.extensions import db, login_manager

def create_app():
    app = Flask(__name__, 
                static_folder='static', 
                template_folder='templates')
    
    # 1. الإعدادات المركزية
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'MAHJOUB_2026_SOVEREIGN')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 2. تهيئة الإضافات من النواة
    db.init_app(app)
    login_manager.init_app(app)

    # 3. تسجيل البلوبرنتات (بعد أن يتم إنشاؤها تلقائياً)
    with app.app_context():
        # هنا سنقوم لاحقاً بتفعيل روابط التطبيقات (apps)
        pass

    return app

app = create_app()

if __name__ == "__main__":
    # تشغيل السيرفر على المنفذ المخصص من Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
