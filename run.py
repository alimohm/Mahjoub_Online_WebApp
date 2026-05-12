from flask import Flask, redirect, url_for
import os
from models.admin_db import db  # استدعاء محرك قاعدة البيانات

# استيراد البوابات (Blueprints) من المسارات المنظمة
from apps.admin_dashboard.routes import admin_bp
from apps.auth_portal.routes import auth_bp

app = Flask(__name__)

# --- إعدادات الحماية والسيادة ---

# المفتاح السري لتشفير الجلسات (Sessions) ومنع التلاعب بالروابط
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026_@_PRIVATE'

# إعداد مسار قاعدة البيانات (يدعم Postgres على Railway أو SQLite محلياً)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- ربط المكونات بالمنظومة ---

# تهيئة قاعدة البيانات مع التطبيق
db.init_app(app)

# تسجيل البوابات ببادئات واضحة (Prefixes)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
from apps.add_supplier.routes import add_supplier_bp
app.register_blueprint(add_supplier_bp)

@app.route('/')
def root():
    """
    نقطة الصفر: توجيه أي دخول مباشر للموقع إلى بوابة تسجيل الدخول 
    لضمان عدم العبور إلا بعد التوثيق.
    """
    return redirect(url_for('auth.login'))

# --- تشغيل المحرك المركزي ---

if __name__ == '__main__':
    # إنشاء الجداول تلقائياً داخل بيئة التطبيق إذا لم تكن موجودة
    with app.app_context():
        db.create_all()
    
    # ضبط المنفذ ليتوافق مع بيئة Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
