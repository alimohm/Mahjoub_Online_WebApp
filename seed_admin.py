# coding: utf-8
# 🛡️ كود تعميد سيادة المالك - محجوب أونلاين 2026

from werkzeug.security import generate_password_hash
from apps import create_app, db
from apps.models.admin_db import AdminUser

app = create_app()

with app.app_context():
    # البحث عن المستخدم "علي محجوب"
    admin = AdminUser.query.filter_by(username='علي محجوب').first()
    
    if admin:
        # ترقية الصلاحيات إلى المالك (Owner)
        admin.role = 'Owner'
        # تحديث كلمة السر إلى 123 مع التشفير الأمني
        admin.password_hash = generate_password_hash('123')
        db.session.commit()
        print("✅ تم تعميد علي محجوب كـ 'المالك' بصلاحيات سيادية كاملة.")
    else:
        # في حال لم يكن الحساب موجوداً، يتم إنشاؤه من الصفر كمالك
        new_owner = AdminUser(
            username='علي محجوب',
            password_hash=generate_password_hash('123'),
            role='Owner'
        )
        db.session.add(new_owner)
        db.session.commit()
        print("✅ تم إنشاء حساب المالك (علي محجوب) بنجاح.")
