# 📂 apps/auth_portal/__init__.py

from flask import Blueprint

# تعريف البلوبرينت (اسم البلوبرينت، اسم الوحدة)
auth_bp = Blueprint('auth_portal', __name__)

# استيراد المسارات (Routes) هنا في الأسفل لتجنب الاستيراد الدائري
from apps.auth_portal import routes

def register_auth_portal(app):
    """تسجيل بلوبرينت المصادقة بشكل آمن"""
    try:
        from apps.auth_portal.routes import auth_portal as auth_routes_bp
        app.register_blueprint(auth_routes_bp, url_prefix='/auth')
        print("✅ تم تسجيل بلوبرينت المصادقة (Auth Portal) بنجاح.")
    except Exception as e:
        print(f"❌ فشل تسجيل بلوبرينت المصادقة: {e}")
