# coding: utf-8
import os
from apps import create_app
from apps.extensions import db
from sqlalchemy import text

# 1. تهيئة التطبيق
app = create_app()

def auto_repair_db():
    """نظام الإصلاح الذاتي المحصن ضد أخطاء بيئة الاختبار."""
    # الحماية: إذا لم يكن هناك اتصال بقاعدة بيانات، نخرج فوراً دون خطأ
    if not os.environ.get("DATABASE_URL"):
        print("ℹ️ نظام الإصلاح: لا يوجد اتصال بقاعدة بيانات، سيتم تخطي الإصلاح (بيئة اختبار).")
        return

    with app.app_context():
        try:
            db.create_all()
            print("✅ تم التأكد من وجود الجداول.")
            
            # (أضف هنا فقط كود إصلاح الأعمدة الخاص بك إذا أردت)
            db.session.commit()
            print("✅ تمت مزامنة الجداول بنجاح.")
            
        except Exception as e:
            print(f"🚨 خطأ في الإصلاح: {e}")
            db.session.rollback()

if __name__ == "__main__":
    # تشغيل الإصلاح فقط عند التشغيل المحلي أو الفعلي
    auto_repair_db()
    
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
