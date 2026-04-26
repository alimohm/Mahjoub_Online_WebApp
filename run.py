import os
from core import create_app, db
from flask import redirect, url_for

# 1. إنشاء نسخة التطبيق عبر دالة المصنع السيادية
app = create_app()

# --- مسار الإيقاظ المركزي (توجيه الحركة عند فتح الرابط الرئيسي) ---
@app.route('/')
def index():
    # توجيه الزائر تلقائياً لبوابة دخول الموردين لضمان استمرارية الحركة
    return redirect(url_for('supplier_panel.login'))

# 2. إدارة هيكل البيانات والتعميد الأولي للحسابات
with app.app_context():
    try:
        # ملاحظة سيادية: تم إيقاف db.drop_all() للحفاظ على بياناتك.
        # استخدمها فقط إذا قمت بتعديل جذري في أعمدة الجداول.
        # db.drop_all() 
        
        # إنشاء الجداول إذا لم تكن موجودة
        db.create_all()
        print("✅ [Database] تم التحقق من الهيكل ومزامنة الأعمدة بنجاح.")

        # استيراد النماذج داخل السياق لضمان تسجيلها بدقة
        from core.models.user import User
        from core.models.supplier import Supplier
        from core.models.product import Product
        
        # --- تعميد حساب القائد (علي محجوب) ---
        # نستخدم دقة عالية في التحقق لضمان دخولك بكلمة "123"
        admin_username = 'علي محجوب'
        admin_user = User.query.filter_by(username=admin_username).first()
        
        if not admin_user:
            new_admin = User(
                username=admin_username, 
                password='123', 
                role='admin'
            )
            db.session.add(new_admin)
            print(f"👤 [Security] تم إنشاء حساب القائد: '{admin_username}' بنجاح.")
        else:
            # تحديث كلمة السر لضمان أنها "123" في حال نسيانها
            admin_user.password = '123'
            print(f"🔐 [Security] تم تأكيد وتحديث كلمة سر القائد '{admin_username}'.")

        # --- تعميد حساب المورد الأول (شريك النجاح التجريبي) ---
        supplier_name = 'مورد تجريبي'
        if not Supplier.query.filter_by(name=supplier_name).first():
            test_supplier = Supplier(
                name=supplier_name, 
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
                is_approved=True, 
                status='active',
                # أرصدة المحفظة السيادية الافتراضية
                wallet_balance=100.0,
                wallet_usd=50.0,
                wallet_sar=150.0,
                wallet_yer=35000.0
            )
            db.session.add(test_supplier)
            db.session.flush() # الحصول على ID المورد لربط المنتجات

            # --- إضافة المنتج التجريبي لربط دورة العمل ---
            test_product = Product(
                name="منتج تجريبي سيادي",
                description="وصف تجريبي للمنتج المرتبط بقمرة",
                q_collection_id="Q-COL-123", 
                cost_price=10.0,
                currency="USD",
                status="pending", 
                supplier_id=test_supplier.id
            )
            db.session.add(test_product)
            print(f"📦 [Sourcing] تم إنشاء حساب المورد '{supplier_name}' ومنتج تجريبي.")

        db.session.commit()
        print("✅ [System] تم حفظ جميع البيانات وتجهيز النظام للإقلاع.")

    except Exception as e:
        print(f"⚠️ [Critical Error] فشل الإقلاع السيادي: {e}")
        db.session.rollback()

if __name__ == "__main__":
    # 3. إعدادات المنفذ لبيئة Railway السحابية
    port = int(os.environ.get("PORT", 8080))
    
    # 4. الإقلاع الرسمي للمنصة
    print(f"🚀 [Mahjoub Online] السيرفر يعمل الآن على المنفذ {port}...")
    
    # host='0.0.0.0' ضروري لاستقبال الطلبات الخارجية على Railway
    app.run(host='0.0.0.0', port=port, debug=False)
