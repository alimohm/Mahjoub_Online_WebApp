import os
from core import create_app, db

# 1. إنشاء تطبيق فلاسك باستخدام المصنع البرمجي (Factory Pattern)
app = create_app()

# 2. نقطة الإقلاع (Entry Point)
if __name__ == "__main__":
    with app.app_context():
        try:
            # محاولة إنشاء الجداول في قاعدة البيانات إذا لم تكن موجودة
            db.create_all()
            print("🏛️ Database connection established & tables created.")
        except Exception as e:
            print(f"⚠️ Database Error: {e}")

    # 3. جلب المنفذ (Port) من إعدادات السيرفر أو استخدام 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    
    # 4. تشغيل التطبيق
    # ملاحظة: في Back4app نستخدم Gunicorn للتشغيل وليس app.run مباشرة
    app.run(host="0.0.0.0", port=port, debug=False)
