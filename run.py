from flask import Flask, redirect, url_for
import os

# 1. استدعاء المرجع الموحد وقادة الجداول
# استيراد الموديلات هنا يضمن أن db.create_all يراهم بوضوح
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

# 2. استيراد البوابات (Blueprints)
try:
    from apps.admin_dashboard.routes import admin_bp
    from apps.auth_portal.routes import auth_bp
    from apps.add_supplier.routes import add_supplier_bp
except ImportError as e:
    print(f"❌ خطأ في استيراد المسارات التقنية: {e}")

app = Flask(__name__)

# --- 3. إعدادات الحماية والسيادة الرقمية ---
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026'

# ضبط وتوافق رابط قاعدة البيانات لبيئة Railway
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- 4. ربط وتعميد المكونات المركزية ---
db.init_app(app)

app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(add_supplier_bp) # المسار: /supplier/add

@app.route('/')
def root():
    return redirect(url_for('auth.login'))

# --- 5. وظيفة بناء الجداول القسرية (Forced Initialization) ---
def setup_database():
    """وظيفة تفرض إنشاء الجداول وتطبع الحالة في السجلات"""
    with app.app_context():
        try:
            print("⏳ بدأت الآن عملية فحص وتعميد الجداول في قاعدة البيانات...")
            
            # إعادة التأكيد على وجود الموديلات داخل السياق
            from models.admin_db import AdminUser
            from models.supplier_db import Supplier
            
            db.create_all()
            print("✅ تم تعميد جميع الجداول (Admin & Supplier) في Postgres بنجاح.")
        except Exception as e:
            print(f"❌ فشل تأسيس المنظومة! السبب: {e}")

# --- 6. تشغيل المحرك المركزي ---
if __name__ == '__main__':
    # تنفيذ التأسيس قبل استقبال أي حركة مرور
    setup_database()
    
    # المنفذ المتوافق مع Railway
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
