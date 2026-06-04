# 📂 reset_db.py - سكربت إعادة بناء القاعدة برمجياً
from apps import create_app
from apps.extensions import db
import shutil
import os

def reset_database():
    print("🚀 جاري البدء بعملية تنظيف الخزينة...")
    
    # 1. حذف مجلد migrations
    if os.path.exists('migrations'):
        shutil.rmtree('migrations')
        print("✅ تم حذف المجلد القديم للمهاجرات.")

    # 2. حذف ملف قاعدة البيانات (إذا كان sqlite)
    # تأكد من تعديل اسم الملف إذا كان مختلفاً عندك
    if os.path.exists('app.db'):
        os.remove('app.db')
        print("✅ تم حذف قاعدة البيانات القديمة.")

    # 3. تشغيل أوامر الفلاسك برمجياً
    from flask_migrate import init, migrate, upgrade
    
    app = create_app()
    with app.app_context():
        print("⚙️ جاري إعادة التهيئة...")
        init()
        print("📦 جاري إنشاء الهيكل السيادي الجديد...")
        migrate(message="Sovereign_Database_Build")
        print("🛠️ جاري ترقية قاعدة البيانات...")
        upgrade()
        print("✨ تم بنجاح! الخزينة جاهزة للعمل.")

if __name__ == '__main__':
    reset_database()
