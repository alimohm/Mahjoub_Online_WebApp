# run.py
# coding: utf-8
# 🔑 مفتاح تشغيل المحرك المركزي - منصة محجوب أونلاين 2026

import os
from apps import create_app

app = create_app()

if __name__ == "__main__":
    # 🌐 التحقق من البيئة: إذا كنا نشتغل محلياً (Development) وليس على السيرفر الخارجي
    if os.environ.get('FLASK_ENV') == 'development' or not os.environ.get('DATABASE_URL'):
        # إجبار السيرفر المحلي على قبول التصفح عبر localhost دون تعارض مع SERVER_NAME
        app.config['SERVER_NAME'] = '127.0.0.1:5000'
        print("💻 تم تشغيل السيرفر في بيئة التطوير المحلية: http://127.0.0.1:5000")
        app.run(debug=True, port=8080)
    else:
        # التشغيل الافتراضي المخصص للسيرفرات السحابية
        app.run()
