import os
from core import create_app, db
from core.models import User, Supplier, Product
from werkzeug.security import generate_password_hash

# إنشاء تطبيق Flask
app = create_app()

def initialize_sovereign_system():
    """
    وظيفة التطهير والتعميد: لإعادة بناء قاعدة البيانات
    وضمان مطابقة الكود للواقع التقني الجديد.
    """
    with app.app_context():
        try:
            print("🔄 [System] جاري تحديث الهيكل السيادي للمجداول...")
            
            # 🚨 تحذير: هذا السطر يمسح البيانات القديمة لضمان تحديث الحقول (مثل description)
            db.drop_all() 
            db.create_all() 
            
            # --- إنشاء حساب القائد العام (علي محجوب) ---
            # نستخدم التشفير لضمان قبول النظام لبيانات الدخول
            hashed_password = generate_password_hash('123') 
            
            admin = User(
                username='علي محجوب', 
                password=hashed_password, 
                role='admin'
            )
            
            # --- إنشاء مورد تجريبي لاختبار الترسانة المالية ---
            test_supplier = Supplier(
                name='مورد تهامة التجريبي', 
                password=generate_password_hash('123'), 
                email='vendor@mahjoub.online',
                is_approved=True,
                status='active',
                # المحافظ السيادية الجديدة
                wallet_balance=0.00,
                wallet_sar=0.00,
                wallet_usd=0.00,
                wallet_yer=0.00
            )
            
            # تعميد البيانات في قاعدة البيانات
            db.session.add(admin)
            db.session.add(test_supplier)
            db.session.commit()
            
            print("✅ [Database] تم تحديث الهيكل بنجاح وحساب القائد جاهز الآن.")
            
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ [Error] فشل التحديث التقني: {e}")

if __name__ == "__main__":
    # تشغيل عملية التحديث لمرة واحدة عند الإقلاع
    # ملاحظة: بمجرد استقرار الموقع، يمكنك وضع علامة # قبل السطر التالي
    initialize_sovereign_system()
    
    # إعدادات المنافذ للتوافق مع السحابة (Railway / Render)
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
