def initialize_sovereignty():
    """
    دالة تعميد وتشييد البنية التحتية لعام 2026:
    تقوم بإنشاء كافة الجداول الناقصة مباشرة داخل سيرفر PostgreSQL الحي.
    """
    with app.app_context():
        try:
            print("⏳ جاري فحص وتعميد جداول النواة في السيرفر الحي...")
            
            # استيراد النماذج بشكل صارم لإجبار قاعدة البيانات على رؤيتها
            from apps.models.supplier_db import Supplier
            from apps.models.wallet_db import SupplierWallet
            from apps.models.admin_db import AdminUser
            
            # أمر التشييد الشامل والسيادي
            db.create_all()
            db.session.commit()
            print("🚀 سيادة وحوكمة: تم فحص قاعدة البيانات وإنشاء جداول الموردين والمحافظ والمشرفين بنجاح تنفيذي مطلق.")
            
            # تأمين حساب المؤسس والمالك السيادي للمنصة
            owner = AdminUser.query.filter_by(username='علي محجوب').first()
            if not owner:
                print("🛡️ جاري تعميد حساب المالك السيادي للمنصة...")
                new_owner = AdminUser(
                    username='علي محجوب',
                    password_hash=generate_password_hash('123'),
                    role='Owner'
                )
                db.session.add(new_owner)
                db.session.commit()
                print("✅ تم تعميد 'علي محجوب' مالكاً رسمياً لنظام الحوكمة الرقمية.")
                
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ تنبيه تقني حرج: تعذر إنشاء الجداول على السيرفر الحي: {e}")
