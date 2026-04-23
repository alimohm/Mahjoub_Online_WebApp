import os
from core import create_app

# 1. إنشاء نسخة التطبيق من المحرك المركزي
# ملاحظة: تعريف db موجود داخل core/__init__.py أو core/models.py 
# ولا يجب تعريفه هنا مرة أخرى
app = create_app()

def prepare_environment():
    """تأمين وجود المجلدات الضرورية في بيئة السيرفر"""
    # Railway يستخدم نظام ملفات مؤقت، لذا نتأكد من وجود المجلد
    temp_path = os.path.join('static', 'img', 'temp_uploads')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)

if __name__ == '__main__':
    prepare_environment()
    
    # 2. الحصول على المنفذ من نظام التشغيل (ضروري لـ Railway)
    port = int(os.environ.get("PORT", 5000))
    
    # 3. تشغيل السيرفر
    # تم إيقاف debug لضمان استقرار العمل على Railway
    app.run(
        host='0.0.0.0', 
        port=port, 
        debug=False
    )
