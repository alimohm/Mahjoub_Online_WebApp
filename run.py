from flask import Flask
from core.models import db
import os

def create_app():
    app = Flask(__name__)
    
    # رابط قاعدة بيانات PostgreSQL السحابية الخاص بك
    # ملاحظة: هذا الرابط يحتوي على كلمة السر، لا تشاركه مع أحد خارج محيط التطوير
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mahjoub_online_1_db_user:S7dxtVGcKwrsM1QEzGOuPPcRL8dKxgXk@dpg-d79tuthr0fns73epej4g-a/mahjoub_online_1_db'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = 'mahjoub_online_key_2026' # مفتاح أمان الجلسات

    # ربط كائن قاعدة البيانات بالتطبيق
    db.init_app(app)

    # مسار مؤقت لاختبار واجهة الدخول
    @app.route('/')
    def index():
        from flask import render_template
        return render_template('admin/login.html')

    return app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        print("⏳ جاري الاتصال بقاعدة البيانات السحابية وتصفيرها...")
        try:
            # مسح كل شيء قديم للبدء على نظافة (كما طلبت)
            db.drop_all()
            # إنشاء الجداول الجديدة (Users, Suppliers, Orders, Logs)
            db.create_all()
            print("✅ تم بنجاح! قاعدة بيانات 'محجوب أونلاين' جاهزة الآن أونلاين.")
        except Exception as e:
            print(f"❌ حدث خطأ أثناء الاتصال: {e}")
            print("تأكد من تثبيت مكتبة psycopg2-binary")

    # تشغيل السيرفر المحلي للتجربة
    app.run(debug=True, port=5000)
