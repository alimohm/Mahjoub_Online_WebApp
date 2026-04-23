import os
from core import create_app

# 1. تهيئة التطبيق باستخدام المحرك المركزي
app = create_app()

def prepare_environment():
    """تجهيز بيئة العمل (إنشاء المجلدات المؤقتة إذا لم توجد)"""
    temp_path = os.path.join('static', 'img', 'temp_uploads')
    if not os.path.exists(temp_path):
        os.makedirs(temp_path)
        print(f"[*] Created temporary directory: {temp_path}")

if __name__ == '__main__':
    # 2. التأكد من جاهزية المجلدات قبل التشغيل
    prepare_environment()
    
    # 3. تشغيل السيرفر
    # host='0.0.0.0' تسمح لك بالوصول للنظام من لابتوب آخر أو عبر الشبكة
    # port=5000 المنفذ الافتراضي للفلاسك
    # debug=True مفيد جداً في مرحلة التطوير لإظهار الأخطاء وتحديث الكود تلقائياً
    print("--- 🚀 Mahjoub Online Engine is Starting ---")
    app.run(
        host='0.0.0.0', 
        port=5000, 
        debug=True
    )
