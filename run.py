# coding: utf-8
from apps import create_app, db
from apps.models.admin_db import AdminUser
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet
from werkzeug.security import generate_password_hash

app = create_app()

def seed_database():
    with app.app_context():
        # فحص وجود المالك لضمان عدم التكرار (حماية الزرع)
        if not AdminUser.query.filter_by(username='ali_mahjoub').first():
            print("🌱 بدء عملية الزرع الأولي (علي محجوب + 21 مورداً)...")

            # 1. إضافة المالك
            admin = AdminUser(username='ali_mahjoub', role='Owner', phone_number='0000000000')
            admin.set_password('123')
            db.session.add(admin)
            db.session.flush()

            # 2. إضافة 21 مورداً مع محافظهم
            for i in range(1, 22):
                new_sup = Supplier(
                    username=f'sup_{i}',
                    password_hash=generate_password_hash('sup_pass_123'),
                    trade_name=f'مؤسسة المورد {i}',
                    owner_name=f'صاحب العمل {i}',
                    owner_phone=f'7700000{i:02d}',
                    wallet_code=f'W-{i}-2026'
                )
                db.session.add(new_sup)
                db.session.flush() # الحصول على الـ ID الخاص بالمورد
                
                # 3. إنشاء محفظة لكل مورد (بأرصدة ابتدائية صفرية)
                wallet = SupplierWallet(
                    supplier_id=new_sup.id, 
                    balance_sar=0.0, 
                    balance_yer=0.0, 
                    balance_usd=0.0
                )
                db.session.add(wallet)

            db.session.commit()
            print("✅ تم الزرع بنجاح: المالك والموردون الـ 21 والمحافظ.")
            print("⚠️ تذكير: بعد التأكد من نجاح الزرع على السيرفر، احذف كود الزرع من هذا الملف.")

if __name__ == "__main__":
    seed_database()
    app.run()
