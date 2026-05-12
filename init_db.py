import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def build_sovereign_infrastructure():
    print("🧹 بدء بروتوكول التطهير والبناء...")
    
    # 1. إنشاء المجلدات (لضمان وجود المسارات)
    structure = ['core/models', 'apps/supplier_app/templates', 'static/css']
    for path in structure:
        os.makedirs(path, exist_ok=True)
        with open(os.path.join(path, '__init__.py'), 'w') as f: pass

    # 2. تهيئة التطبيق المؤقت للبناء
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)

    with app.app_context():
        try:
            # استيراد الموديل الجديد (تأكد من رفعه في core/models/supplier_db.py)
            from core.models.supplier_db import Supplier
            
            print("⚠️ حذف الجداول القديمة لمنع التصادم...")
            db.drop_all() # هذا الأمر سيمسح كل الجداول القديمة
            
            print("💎 بناء الجداول الجديدة بالهيكل السيادي...")
            db.create_all() # سيقوم ببناء الجداول بناءً على الموديل الجديد
            
            print("✅ اكتمل التطهير والتأسيس بنجاح.")
        except Exception as e:
            print(f"❌ فشل في التطهير: {e}")

if __name__ == "__main__":
    build_sovereign_infrastructure()
