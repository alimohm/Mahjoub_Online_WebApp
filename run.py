from flask import Flask, redirect, url_for
import os
# استدعاء محركات قواعد البيانات والموديلات لضمان التأسيس الكامل
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier # إضافة موديل الموردين هنا لضمان ظهور الجدول

# استيراد البوابات (Blueprints)
from apps.admin_dashboard.routes import admin_bp
from apps.auth_portal.routes import auth_bp
from apps.add_supplier.routes import add_supplier_bp

app = Flask(__name__)

# --- إعدادات الحماية والسيادة ---

# المفتاح السري لتشفير الجلسات ومنع التلاعب
app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026_@_PRIVATE'

# إعداد مسار قاعدة البيانات (دعم كامل لـ Postgres على Railway)
database_url = os.environ.get('DATABASE_URL')
if database_url and database_url.startswith("postgres://"):
    database_url = database_url.replace("postgres://", "postgresql://", 1)

app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- ربط المكونات بالمنظومة ---

db.init_app(app)

# تسجيل البوابات ببادئات واضحة لضمان التنظيم وتجنب تكرار /admin/admin
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(add_supplier_bp) # تمت إزالة البادئة هنا لأنها معرفة داخل الـ Blueprint

@app.route('/')
def root():
    """ توجيه تلقائي لبوابة الدخول لضمان الهوية السيادية للمنصة """
    return redirect(url_for('auth.login'))

# --- تهيئة المنظومة وإنشاء الجداول والحساب القيادي ---

def setup_database():
    with app.app_context():
        # إنشاء كافة الجداول (المسؤولين والموردين) فوراً عند التشغيل
        db.create_all() 
        print("✅ تم تعميد كافة الجداول (Admin + Suppliers) في قاعدة البيانات.")
        
        # التأكد من وجود حساب المؤسس "علي محجوب"
        check_admin = AdminUser.query.filter_by(username='ali_mahjoub').first()
        if not check_admin:
            founder = AdminUser(
                username='ali_mahjoub',
                full_name='علي محجوب',
                role='founder'
            )
            founder.set_password('123') 
            db.session.add(founder)
            db.session.commit()
            print("🛡️ تم تأمين حساب المؤسس علي محجوب في المنظومة بنجاح.")

# --- تشغيل المحرك المركزي ---

if __name__ == '__main__':
    setup_database() # تنفيذ تهيئة البيانات والتحقق من الجداول قبل تشغيل السيرفر
    
    # ضبط المنفذ ليتوافق مع بيئة Railway السحابية
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
