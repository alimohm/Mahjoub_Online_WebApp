# coding: utf-8
# 🚀 ملف التشغيل الرئيسي للنواة - محجوب أونلاين 2026
import os
import sys
from apps import create_app

# إنشاء التطبيق
app = create_app()

# فحص أمني: التأكد من وجود مفتاح التشفير قبل الإقلاع
if not app.config.get('ENCRYPTION_KEY') and not os.environ.get('ENCRYPTION_KEY'):
    print("❌ خطأ حرج: ENCRYPTION_KEY غير موجود في الإعدادات أو متغيرات البيئة!")
    sys.exit(1) # إيقاف التشغيل فوراً لمنع حدوث أخطاء فك التشفير

print("✅ المصنع المركزي للنواة يعمل بنجاح!")
print("🛡️ نظام التشفير (AES-256) مفعل وجاهز.")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
