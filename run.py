import os
from core import create_app, db
from flask import redirect, url_for

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('supplier_panel.login'))

with app.app_context():
    try:
        # إنشاء الجداول لضمان وجود الهيكل
        db.create_all()
        
        from core.models.user import User
        from core.models.supplier import Supplier
        
        # 1. --- تعميد القائد (علي محجوب) ---
        admin = User.query.filter_by(username='علي محجوب').first()
        if not admin:
            admin = User(username='علي محجوب', password='123', role='admin')
            db.session.add(admin)
            print("👤 [Security] تم إنشاء حساب القائد 'علي محجوب' بنجاح.")
        else:
            admin.password = '123' # تأمين كلمة السر
            print("🔐 [Security] تم تحديث كلمة سر القائد إلى 123.")

        # 2. --- تعميد المورد التجريبي ---
        # نستخدم 'name' هنا لأنه المعرف في verify_supplier_credentials
        supplier = Supplier.query.filter_by(name='مورد تجريبي').first()
        if not supplier:
            new_supplier = Supplier(
                name='مورد تجريبي',
                password='123',
                email='test@mahjoub.online',
                trade_name='مؤسسة التجربة السيادية',
                is_approved=True,
                status='active',
                province='الحديدة',
                district='الخوخة'
            )
            db.session.add(new_supplier)
            print("📦 [Sourcing] تم إنشاء حساب 'مورد تجريبي' بنجاح.")
        else:
            supplier.password = '123' # تأمين كلمة السر للمورد
            supplier.is_approved = True # ضمان التفعيل
            print("🔐 [Sourcing] تم تحديث كلمة سر المورد التجريبي إلى 123.")

        db.session.commit()
        print("✅ [System] تم تعميد الحسابات السيادية بنجاح.")

    except Exception as e:
        db.session.rollback()
        print(f"⚠️ [Error] فشل في تهيئة البيانات: {e}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port, debug=False)
