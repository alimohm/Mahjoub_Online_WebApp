import os
from core import create_app, db
from core.models import User, Supplier, Product
from werkzeug.security import generate_password_hash

# إنشاء تطبيق Flask بالهوية السيادية
app = create_app()

def initialize_sovereign_system():
    """
    وظيفة التطهير والتعميد: لإعادة بناء قاعدة البيانات
    وضمان مطابقة الكود للواقع التقني الجديد والمحافظ المالية.
    """
    with app.app_context():
        try:
            print("🔄 [System] جاري تطهير وإعادة بناء الهيكل السيادي...")
            
            # 🚨 تحذير: مسح شامل لضمان تحديث الحقول الجديدة (مثل المحافظ والمناطق)
            db.drop_all() 
            db.create_all() 
            
            # --- 1. تعميد حساب القائد العام (علي محجوب) ---
            # استخدام التشفير الأمني العالي لضمان قبول الدخول
            hashed_admin_pass = generate_password_hash('123') 
            
            admin = User(
                username='علي محجوب', 
                password=hashed_admin_pass, 
                role='admin'
            )
            
            # --- 2. إنشاء مورد تجريبي متكامل الأركان ---
            test_supplier = Supplier(
                name='مورد تهامة التجريبي', 
                password=generate_password_hash('123'), 
                email='vendor@mahjoub.online',
                trade_name='مؤسسة تهامة للتجارة',
                province='الحديدة', # الحقل الجغرافي الذي كان يسبب الخطأ
                phone='770000000',
                is_approved=True,
                status='active',
                # تصفير المحافظ السيادية لبدء النشاط التجاري
                wallet_balance=0.00,
                wallet_sar=0.00,
                wallet_usd=0.00,
                wallet_yer=0.00
            )
            
            # حفظ البيانات في الخزانة المركزية
            db.session.add(admin)
            db.session.add(test_supplier)
            db.session.commit()
            
            print("✅ [Database] تم بناء الهيكل بنجاح. حساب القائد والمورد التجريبي جاهزان!")
            
        except Exception as e:
            db.session.rollback()
            print(f"⚠️ [Error] فشل في عملية التطهير والتعميد: {e}")

if __name__ == "__main__":
    # تشغيل عملية التهيئة (يتم تفعيلها عند كل ريستارت للسيرفر في Railway)
    initialize_sovereign_system()
    
    # ضبط المنفذ العالمي لضمان الربط مع Railway/Render
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)
