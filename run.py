# coding: utf-8
# 🌟 توثيق: هذا الملف هو نقطة الانطلاق الرئيسية للمنصة على خوادم Railway
import os
from flask import Flask, redirect, url_for
from models.admin_db import db  # استيراد كائن قاعدة البيانات الموحد

def create_app():
    """
    دالة بناء التطبيق (Application Factory): 
    تقوم بتجهيز الإعدادات، ربط قاعدة البيانات، وتفعيل محرك Jinja2 للقوالب.
    """
    # 1. تهيئة التطبيق وتحديد مسار مجلد القوالب (Templates)
    app = Flask(__name__, template_folder='apps/templates')
    
    # 2. إعداد مفتاح الأمان (Secret Key) لتشفير بيانات الجلسات
    app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_SECURE_2026'

    # 3. ضبط إعدادات قاعدة البيانات (PostgreSQL للإنتاج أو SQLite للتجربة)
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        # تصحيح البروتوكول ليتوافق مع SQLAlchemy
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # 4. ربط قاعدة البيانات بالتطبيق
    db.init_app(app)

    # 5. تسجيل الروابط (Blueprints) لربط الصفحات ببعضها
    from apps.auth_portal.routes import auth_bp
    from apps.admin_dashboard.routes import admin_dashboard  
    from apps.add_supplier.routes import admin_suppliers

    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_dashboard, url_prefix='/admin')
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # 6. إنشاء الجداول تلقائياً عند تشغيل النظام لأول مرة
    with app.app_context():
        db.create_all()

    # 7. مسار توجيهي: عند الدخول للرابط الرئيسي، يتم التحويل لصفحة الدخول
    @app.route('/')
    def root():
        return redirect(url_for('auth_portal.login')) 

    return app

# 🔑 هام جداً: تعريف المتغير 'app' عالمياً ليتمكن Gunicorn من رؤيته وتشغيله
app = create_app()

if __name__ == '__main__':
    # تحديد المنفذ تلقائياً بناءً على بيئة التشغيل (Railway يستخدم 8080 غالباً)
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
