# apps/__init__.py
# coding: utf-8

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
# استيراد كلاس الإعدادات الرئيسي لتهيئة السيرفر وقاعدة البيانات
from config import Config 

# 1️⃣ أولاً: إنشاء كائنات الإضافات (Extensions) وتصديرها فوراً للذاكرة
db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    
    # 2️⃣ ثانياً: تحميل الإعدادات أولاً لحقن URI قاعدة البيانات (لمنع خطأ RuntimeError)
    app.config.from_object(Config)

    # 3️⃣ ثالثاً: ربط الكائنات مع التطبيق بعد استقرار الإعدادات في الذاكرة
    db.init_app(app)
    login_manager.init_app(app)

    # -------------------------------------------------------------------------
    # 4️⃣ رابعاً: منطقة تسجيل المسارات والموديلات والـ Blueprints (آمنة تماماً)
    # -------------------------------------------------------------------------
    
    # استدعاء الموديل لتهيئة وربط الجداول في قاعدة البيانات بشكل مستقر
    from apps.models.supplier_db import Supplier

    # [أ] تسجيل مسار محرك تعميد وإضافة الموردين الجديد
    from apps.add_supplier.routes import admin_suppliers
    app.register_blueprint(admin_suppliers, url_prefix='/admin/suppliers')

    # [ب] تسجيل مسار بوابة المصادقة وتسجيل الدخول (بوابة auth_portal)
    # لخدمة القالب: apps/auth_portal/templates/auth/login.html
    from apps.auth_portal.routes import auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    # [ج] تسجيل مسار لوحة التحكم الرئيسية ومحتواها (admin_dashboard)
    # لخدمة القالب: apps/admin_dashboard/templates/admin/dashboard_content.html
    from apps.admin_dashboard.routes import admin_dashboard_blueprint
    app.register_blueprint(admin_dashboard_blueprint, url_prefix='/admin/dashboard')

    # [د] تسجيل المسارات العامة للمنصة وهيكلها الأساسي
    # لخدمة القالب المشترك: apps/templates/admin_base.html
    # ملاحظة: القوالب داخل مجلد apps/templates تقرأ تلقائياً عبر الـ Jinja2 (extends)
    # وإذا كان لديك ملف مسارات رئيسي للواجهة يتم تسجيله هنا:
    try:
        from apps.main_routes import main_blueprint
        app.register_blueprint(main_blueprint)
    except ImportError:
        # إذا كانت المسارات الرئيسية تدار من ملف آخر، يمكنك تفعيله هنا
        pass

    return app
