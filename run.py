import os
from core import create_app

# إنشاء نسخة التطبيق من مجلد "العاصمة" core
app = create_app()

if __name__ == '__main__':
    # الحصول على المنفذ (Port) ديناميكياً من بيئة Render أو Railway
    # القيمة الافتراضية 10000 هي المناسبة لـ Render
    port = int(os.environ.get("PORT", 10000))
    
    # تشغيل السيرفر ليكون متاحاً للإنترنت (host='0.0.0.0')
    # تعطيل الـ debug لضمان أمان وحماية بيانات "شركاء النجاح"
    app.run(host='0.0.0.0', port=port, debug=False)
