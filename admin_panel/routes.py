from core import create_app, db
import os

# 1. إنشاء نسخة التطبيق عبر دالة المصنع
# هذه الدالة تقوم بتسجيل Blueprints الإدارة والموردين تلقائياً
app = create_app()

# 2. تهيئة قاعدة البيانات والتأكد من الجداول
with app.app_context():
    try:
        # إنشاء الجداول الناقصة في قاعدة بيانات Render
        db.create_all()
        print("✅ [Database] Connection verified and tables are ready.")
    except Exception as e:
        # طباعة الخطأ في السجلات السوداء للتشخيص إذا فشل الربط
        print(f"⚠️ [Database] Startup Note: Could not connect or create tables: {e}")

if __name__ == "__main__":
    # 3. جلب المنفذ (Port) المخصص من Railway
    # نستخدم 8080 كقيمة افتراضية إذا لم يتوفر المتغير البيئي
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل السيرفر
    # host='0.0.0.0' ضروري جداً لاستقبال الطلبات الخارجية من الإنترنت
    print(f"🚀 Mahjoub Online is launching on port {port}...")
    
    # debug=False هو الخيار الصحيح للرفع الفعلي (Production) لضمان الأداء
    app.run(host='0.0.0.0', port=port, debug=False)
