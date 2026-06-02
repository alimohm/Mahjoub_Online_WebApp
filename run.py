# 📂 run.py - نسخة التشخيص الجذري
import sys
import traceback
from apps import create_app

print("🚀 بدء تشغيل تطبيق محجوب أونلاين...")

try:
    # محاولة إنشاء التطبيق
    app = create_app()
    print("✅ تم إنشاء كائن التطبيق بنجاح.")
    
    # التحقق من أن التطبيق يعمل فعلياً
    if app:
        print("🎉 التطبيق جاهز للإقلاع بواسطة Gunicorn.")
    else:
        print("❌ التطبيق لم يعد أي شيء (None)!")
        sys.exit(1)

except Exception as e:
    print("🚨 كارثة حرجة عند تشغيل create_app:")
    traceback.print_exc() # هذا السطر سيجبر Render على كتابة الخطأ الحقيقي في السجلات
    sys.exit(1) # إغلاق التطبيق برمز خطأ ليظهر في الـ Logs
