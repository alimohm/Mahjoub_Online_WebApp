import os
from core import create_app, db

# 1. إنشاء نسخة التطبيق عبر دالة المصنع
app = create_app()

# 2. إدارة قاعدة البيانات وإنشاء الحسابات السيادية
with app.app_context():
    try:
        # ملاحظة للقائد: سنستخدم drop_all لمرة واحدة فقط لمسح الهيكل القديم المتعارض
        # db.drop_all() # فك التعليق عن هذا السطر فقط إذا واجهت خطأ في الدخول أول مرة
        
        # إنشاء الجداول بالحقول الجديدة (النشاط، الموقع، المحفظة)
        db.create_all()
        print("✅ [Database] تم مزامنة الجداول السيادية (MAH-9046) بنجاح.")

        # استيراد موديلات المستخدمين
        from core.models import User, Supplier
        
        # --- إنشاء حساب القائد السيادي (Admin) ---
        admin_username = 'علي محجوب'
        if not User.query.filter_by(username=admin_username).first():
            new_admin = User(
                username=admin_username, 
                password='123', 
                role='admin'
            )
            db.session.add(new_admin)
            print(f"👤 [Security] تم تعميد حساب القائد '{admin_username}'.")

        # --- إنشاء حساب شريك النجاح (المورد العربي المطور) ---
        supplier_display_name = 'مورد تجريبي'
        if not Supplier.query.filter_by(name=supplier_display_name).first():
            test_supplier = Supplier(
                name=supplier_display_name, 
                email='test@supplier.com',
                password='123',
                activity_type='إلكترونيات وتقنية',
                trade_name='ترسانة محجوب الرقمية',
                full_name='علي محجوب (تجريبي)',
                province='الحديدة',
                district='الخوخة',
                phone='777777777',
                fin_type='banks',
                bank_name='بنك الكريمي الإسلامي',
                bank_acc='MAH-ACC-9046',
                wallet_balance=100.0
            )
            db.session.add(test_supplier)
            print(f"📦 [Sourcing] تم إنشاء حساب المورد السيادي '{supplier_display_name}'.")

        db.session.commit()
        print("✅ [System] تم حفظ جميع البيانات وتجهيز المحفظة اللامركزية.")

    except Exception as e:
        print(f"⚠️ [Critical] تنبيه أثناء الإقلاع السيادي: {e}")

if __name__ == "__main__":
    # 3. إعدادات المنفذ لـ Railway
    port = int(os.environ.get("PORT", 8080))
    
    # 4. الإقلاع الرسمي لمنصة محجوب أونلاين
    print(f"🚀 [Mahjoub Online] المنصة اللامركزية تعمل الآن على المنفذ {port}...")
    app.run(host='0.0.0.0', port=port, debug=False)
