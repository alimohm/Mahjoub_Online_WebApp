from flask import Flask, redirect, url_for
import os

# الاستدعاء من المسارات الجديدة بعد إضافة __init__.py
from apps.admin_dashboard.routes import admin_bp
from apps.auth_portal.routes import auth_bp

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_KEY_2026'

# تسجيل الأنظمة ببادئات واضحة
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')

@app.route('/')
def root():
    # التحويل التلقائي للبوابة عند تشغيل المنصة
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    # التشغيل على المنفذ المتوافق مع Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
