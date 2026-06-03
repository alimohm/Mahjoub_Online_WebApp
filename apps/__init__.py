# coding: utf-8
# 📂 apps/__init__.py - المصنع الرئيسي المحمي والمحصن للتطبيق

from flask import Flask, redirect, url_for
from config import Config
from werkzeug.middleware.proxy_fix import ProxyFix
from apps.extensions import db, login_manager

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # 🛡️ إعداد ProxyFix لضبط البروتوكولات والـ IPs في بيئة Render
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    # تهيئة الإضافات الأساسية
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth_portal.login' 

    with app.app_context():
        # 1. تهيئة قاعدة البيانات بأسلوب مرن ومقاوم للانهيار
        try:
            from apps.models.admin_db import AdminUser
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import SupplierWallet, WalletTransaction
            from apps.models.settlements_db import AdminSettlement
            from apps.models.statement_db import SupplierStatement
            db.create_all()
            print("⚡ [Database] تم بناء ومزامنة الجداول بنجاح.")
        except Exception as e:
            print(f"❌ [Database Error] فشل تهيئة قاعدة البيانات: {e}")

        # 2. تهيئة لودر المستخدم (User Loader) لإدارة الجلسات
        @login_manager.user_loader
        def load_user(user_id):
            return AdminUser.query.get(int(user_id)) if user_id else None

        # 3. تسجيل المسارات (Blueprints) بأسلوب الحلقات الآمنة
        blueprints = [
            ('apps.auth_portal.routes', 'auth_blueprint', ''),
            ('apps.add_supplier.routes', 'add_supplier', '/suppliers'),
            ('apps.financial_ops.routes', 'financial_blueprint', '/financial_ops'),
            ('apps.statement.routes', 'statement_blueprint', '/statement'),
            ('apps.admin_dashboard.routes', 'admin_dashboard', '/admin')
        ]

        for module_path, bp_name, prefix in blueprints:
            try:
                module = __import__(module_path, fromlist=[bp_name])
                blueprint = getattr(module, bp_name)
                app.register_blueprint(blueprint, url_prefix=prefix)
                print(f"✅ تم تسجيل {bp_name} بنجاح.")
            except Exception as e:
                print(f"⚠️ [Warning] فشل تسجيل {bp_name}، السيرفر سيستمر بالعمل: {e}")
        
        # 4. توجيه المسار الرئيسي بالتطبيق ديناميكياً للمسار السري الذكي
        @app.route('/')
        def root_redirect():
            return redirect(url_for('auth_portal.login'))

        # 🤖 [الطبقة الأولى] مسار ديناميكي لملف robots.txt لمنع زحف البوتات
        @app.route('/robots.txt')
        def robots_txt():
            response = app.make_response("User-agent: *\nDisallow: /")
            response.headers["Content-Type"] = "text/plain"
            return response

        # 🛡️ [الطبقة الثانية] حقن جدار الحماية السيادي (Security Headers) لرفع التقييم لـ (أ)
        @app.after_request
        def add_security_headers(response):
            # أ. منع الأرشفة والحفظ نهائياً في خوادم البحث والكاش (Google Cache)
            response.headers["X-Robots-Tag"] = "noindex, nofollow, noarchive, nosnippet"
            
            # ب. حماية ضد ثغرات Clickjacking ومنع وضع السيرفر داخل إطارات خارجية (iFrames)
            response.headers["X-Frame-Options"] = "DENY"
            
            # ج. منع المتصفح من تخمين نوع الملفات لحظر الملفات الخبيثة المتخفية
            response.headers["X-Content-Type-Options"] = "nosniff"
            
            # د. أمن النقل المشدد (HSTS) - إجبار المتصفح على الاتصال المشفر دائماً لمدة سنة كاملة
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains; preload'
            
            # هـ. سياسة أمان المحتوى (CSP) - حظر حقن الأكواد الخبيثة مع السماح بسحابة Qomra وواجهات Meta
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' 'unsafe-eval' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://fonts.gstatic.com https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "img-src 'self' data: https:; "
                "connect-src 'self' https://api.qumra.cloud https://graph.facebook.com;"
            )
            
            # و. سياسة الإحالة (Referrer Policy) - حماية بيانات الرابط السري من التسريب للخارج عند الانتقال لروابط أخرى
            response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
            
            # ز. سياسة الأذونات (Permissions Policy) - إغلاق الكاميرا والموقع الجغرافي تماماً لقطع أي محاولة استغلال
            response.headers['Permissions-Policy'] = 'geolocation=(), camera=(), microphone=(), payment=()'
            
            return response

    return app
