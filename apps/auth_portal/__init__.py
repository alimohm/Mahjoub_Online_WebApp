# 📂 apps/auth_portal/__init__.py

from flask import Blueprint

# تعريف البلوبرينت
# تأكد أن اسم البلوبرينت هنا هو نفسه الذي تستخدمه في routes.py
auth_blueprint = Blueprint('auth_portal', __name__, template_folder='templates')

# لا تستورد الـ routes هنا في الأعلى لتجنب الاستيراد الدائري
# الاستيراد سيتم داخل دالة التسجيل إذا لزم الأمر، أو يكتفي Flask بالتعرف عليه عبر البلوبرينت

def register_auth_portal(app):
    """تسجيل بلوبرينت المصادقة"""
    try:
        # هنا نستورد الـ routes فقط عند الحاجة لتسجيل المسارات
        from apps.auth_portal.routes import auth_blueprint
        app.register_blueprint(auth_blueprint, url_prefix='')
        print("✅ تم تسجيل بلوبرينت المصادقة (Auth Portal) بنجاح.")
    except Exception as e:
        print(f"❌ فشل تسجيل بلوبرينت المصادقة: {e}")
