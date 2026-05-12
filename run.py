from flask import Flask, redirect, url_for
import os

# استيراد البوابات (Blueprints) من المسارات التي قمت بإعدادها
from apps.admin_dashboard.routes import admin_bp
from apps.auth_portal.routes import auth_bp

app = Flask(__name__)

# المفتاح السري لتشفير الجلسات وحماية الروابط
# تم ضبطه ليكون قابلاً للتغير عبر إعدادات Railway لزيادة الأمان
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_KEY_2026_@_PRIVATE'

# تسجيل بوابات المنظومة مع تحديد بادئة الروابط لكل منها
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def root():
    """
    النقطة الصفرية: تقوم بتوجيه أي زائر يدخل للموقع 
    مباشرة إلى بوابة تسجيل الدخول لضمان الحماية.
    """
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # ضبط المنفذ (Port) ليتوافق مع بيئة التشغيل السحابية Railway
    port = int(os.environ.get('PORT', 5000))
    # التشغيل على العنوان 0.0.0.0 ليسمح بالوصول الخارجي للمنصة
    app.run(host='0.0.0.0', port=port)
