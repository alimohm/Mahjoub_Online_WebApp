# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from apps.models.admin_db import AdminUser

# 1. تهيئة التطبيق
app = create_app()

def auto_repair_db():
    """حارس قاعدة البيانات: يتأكد من الهيكل والمدير دون التسبب في تعارض."""
    # الحماية: التخطي التام إذا كنا في بيئة GitHub
    if os.environ.get("GITHUB_ACTIONS"):
        return

    with app.app_context():
        try:
            # إنشاء الجداول إذا لم تكن موجودة
            db.create_all()
            
            # التأكد من الهوية السيادية (محجوب)
            admin = AdminUser.query.filter_by(username="محجوب").first()
            if not admin:
                new_admin = AdminUser(username="محجوب", phone_number="0000000000", role='Owner')
                new_admin.set_password("123")
                db.session.add(new_admin)
                db.session.commit()
                print("✅ تم تثبيت الهوية السيادية (محجوب).")
            
        except Exception as e:
            # رول باك لحماية قاعدة البيانات من أي عمليات غير مكتملة
            db.session.rollback()
            print(f"🚨 خطأ في التهيئة: {e}")

if __name__ == "__main__":
    # تشغيل الحارس
    auto_repair_db()
    
    # تشغيل التطبيق
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
