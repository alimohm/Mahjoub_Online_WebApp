from core import create_app
import os

# إنشاء نسخة التطبيق
app = create_app()

if __name__ == "__main__":
    # الحصول على المنفذ من إعدادات ريلواي أو استخدام 8080 كافتراضي
    port = int(os.environ.get("PORT", 8080))
    # تشغيل التطبيق (للتطوير المحلي فقط، Gunicorn سيتولى الأمر في السيرفر)
    app.run(host="0.0.0.0", port=port)
