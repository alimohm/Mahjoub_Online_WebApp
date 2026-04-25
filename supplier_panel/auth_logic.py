# التعديل: استيراد الموديل مباشرة من ملفه لضمان الاستقرار
from core.models.supplier import Supplier

def verify_supplier_credentials(username, password):
    """
    منطق التحقق الخاص بالمنصة اللامركزية لمحجوب أونلاين.
    هذا المحرك يفحص الهوية السيادية للمورد قبل السماح له بدخول الترسانة.
    إرجاع: (الرسالة، نوع التنبيه، كائن المورد أو None)
    """
    try:
        # 1. البحث عن المورد عبر "اسم الدخول" 
        # ملاحظة سيادية: جلب البيانات مع تنظيف الفراغات المحتملة
        supplier = Supplier.query.filter_by(name=username.strip() if username else "").first()

        # 2. فحص الوجود
        if not supplier:
            return '⚠️ عذراً، هذا الاسم غير مسجل في المنصة اللامركزية لمحجوب أونلاين.', 'danger', None

        # 3. فحص كلمة المرور
        # يتم تحويل كلمة المرور لنص وتجريدها من الفراغات لضمان المطابقة
        stored_password = str(supplier.password).strip() if supplier.password else ""
        provided_password = str(password).strip() if password else ""

        if stored_password != provided_password:
            return '❌ كلمة المرور غير صحيحة، يرجى إعادة التثبت من مفاتيح الدخول.', 'warning', None

        # 4. النجاح المطلق
        # يتم إرجاع كائن المورد بالكامل لكي يتم استخدامه في جلسة (Session) المورد
        return f'✅ مرحباً بك يا {supplier.name}.. تم التحقق من الهوية السيادية بنجاح.', 'success', supplier

    except Exception as e:
        # تسجيل الخطأ في السيرفر للمراجعة (Terminal)
        print(f"❌ [Logic Error] فشل في عملية التحقق السيادي: {e}")
        return f'⚠️ حدث خطأ تقني في نظام التحقق: {str(e)}', 'danger', None
