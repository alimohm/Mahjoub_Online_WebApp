# coding: utf-8
# 🚀 ملف التشغيل الرئيسي للنواة - محجوب أونلاين 2026
import os
import sys
from apps import create_app

# تهيئة كائن التطبيق بشكل مباشر ليكون مكشوفاً لـ gunicorn في بيئة الإنتاج
app = create_app()

# رسالة تأكيدية تظهر في الـ Logs عند نجاح المصنع
print("✅ المصنع المركزي للنواة يعمل بنجاح!")

if __name__ == "__main__":
    # الحصول على المنفذ من متغيرات البيئة 
    port = int(os.environ.get("PORT", 5000))
    
    # التشغيل المحلي أو الاحتياطي
    app.run(host="0.0.0.0", port=port, debug=False)
