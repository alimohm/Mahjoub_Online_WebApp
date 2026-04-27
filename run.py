from core import app
import os

if __name__ == "__main__":
    # الحصول على المنفذ (Port) من إعدادات السيرفر، أو استخدام 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    
    # تشغيل التطبيق
    # ملاحظة: في بيئة الإنتاج (Production)، سيستخدم السيرفر Gunicorn
    # ولكن هذا الملف ضروري كمدخل أساسي للمشروع
    app.run(host='0.0.0.0', port=port)
