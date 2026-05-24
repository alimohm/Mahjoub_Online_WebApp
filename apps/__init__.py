# coding: utf-8
from flask import Flask
from apps.extensions import db, login_manager
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix

def create_app():
    """
    دالة المصنع (Application Factory) لإنشاء تطبيق Flask وتأمين بواباته.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # 🚀 معالجة الـ Proxy لبيئات الإنتاج (Railway) لمنع تفكك الجلسة وحلقة التوجيه
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    # تهيئة الإضافات المركزية
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    @login_manager.user_loader
    def load_user(user_id):
        from apps.models.admin_db import AdminUser
        return AdminUser.query.get(int(user_id))

    # 📥 استدعاء الموديلات وتسجيل المسارات داخل سياق التطبيق فوراً عند الإقلاع
    with app.app_context():
        try:
            # 1️⃣ تسجيل الجداول تلقائياً في قاعدة البيانات إذا لم تكن موجودة
            from apps.models import admin_db
            from apps.wallet import models
            db.create_all()

            # 2️⃣ تسجيل الـ Blueprint الخاص بالمحافظ والتسويات المطور
            from apps.wallet import wallet_blueprint
            app.register_blueprint(wallet_blueprint, url_prefix='/wallet')

            # 3️⃣ 🌟 تسجيل الـ Blueprint الخاص بشركاء النجاح والموردين (لحل الـ 404)
            # ملاحظة: تأكد من اسم المجلد الفعلي والملف؛ إذا كان داخل admin_dashboard أو add_supplier
            from apps.admin_dashboard.routes import admin_dashboard_blueprint # مثال حسب هيكلتك
            app.register_blueprint(admin_dashboard_blueprint)
            
            # إذا كان لتعميد الموردين ملف مستقل، قم باستيراده وتسجيله هنا:
            # from apps.suppliers.routes import add_supplier_blueprint
            # app.register_blueprint(add_supplier_blueprint, url_prefix='/suppliers')

        except Exception as e:
            print(f"⚠️ Blueprint Registration Warning: {e}")

    # بوابـة الدخـول المباشرة لـ Gunicorn لمنع الـ Crash
    return app

# الإبقاء على كائن الدخول السيادي مستقراً في الخادم
app = create_app()
