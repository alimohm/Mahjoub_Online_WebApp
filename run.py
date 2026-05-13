from flask import Flask, redirect, url_for
import os
from models.admin_db import db, AdminUser
from models.supplier_db import Supplier

def create_app():
    app = Flask(__name__)
    
    # إعدادات الحماية (SECRET_KEY)
    app.secret_key = os.environ.get('SECRET_KEY') or 'MAHJOUB_CENTRAL_SECURE_2026'

    # إعداد قاعدة البيانات
    database_url = os.environ.get('DATABASE_URL')
    if database_url and database_url.startswith("postgres://"):
        database_url = database_url.replace("postgres://", "postgresql://", 1)
    
    app.config['SQLALCHEMY_DATABASE_URI'] = database_url or 'sqlite:///mahjoub_admin.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # تسجيل البوابات الرقمية (Blueprints)
    from apps.auth_portal.routes import auth_bp
    
    # التصحيح الحاسم: تأكد أن اسم الملف والمجلد صحيح
    try:
        from apps.admin_dashboard.routes import admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')
    except ImportError:
        # حل احتياطي في حال كان الـ Blueprint داخل المجلد يسمى admin_suppliers
        from apps.admin_dashboard.routes import admin_suppliers as admin_bp
        app.register_blueprint(admin_bp, url_prefix='/admin')

    app.register_blueprint(auth_bp, url_prefix='/auth')

    with app.app_context():
        try:
            db.create_all()
            
            # زراعة مستخدم المالك (علي محجوب)
            owner = AdminUser.query.filter_by(username='ali_mahjoub').first()
            if not owner:
                new_admin = AdminUser(
                    username='ali_mahjoub',
                    full_name='علي محجوب',
                    role='founder'
                )
                new_admin.set_password('123') 
                db.session.add(new_admin)
                db.session.commit()
                print("👑 تم زراعة مستخدم المالك 'علي محجوب' بنجاح.")
            else:
                print("✅ مستخدم المالك موجود مسبقاً.")
                
        except Exception as e:
            print(f"⚠️ خطأ أثناء إعداد البيانات: {e}")

    @app.route('/')
    def root():
        # تأكد أن اسم الـ Blueprint هو 'auth' وليس 'auth_bp' في ملف الـ routes الخاص به
        try:
            return redirect(url_for('auth.login'))
        except:
            return redirect('/auth/login')

    return app

app = create_app()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)
