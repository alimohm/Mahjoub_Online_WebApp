# 📂 inject_admin.py
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser

def inject_sovereign_admin():
    app = create_app()
    with app.app_context():
        # بيانات الدخول المطلوبة
        u, p, ph = "mahjoub", "123", "0000000000"
        
        # التحقق من وجود المستخدم
        existing = AdminUser.query.filter_by(username=u).first()
        if existing:
            print(f"⚠️ المستخدم {u} موجود مسبقاً في قاعدة البيانات.")
            return

        # إنشاء الهوية السيادية
        new_admin = AdminUser(username=u, phone_number=ph, role='Owner')
        # التشفير هنا سيقوم بتحويل '123' إلى رمز مشفر غير قابل للقراءة
        new_admin.set_password(p) 
        
        db.session.add(new_admin)
        db.session.commit()
        print(f"✅ تم حقن الهوية السيادية بنجاح للمستخدم: {u}")
        print("🔒 ملاحظة: تم تخزين كلمة المرور مشفرة كـ (Hash) في قاعدة البيانات.")

if __name__ == "__main__":
    inject_sovereign_admin()
