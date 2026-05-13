from flask import render_template
from . import admin_dashboard  # استيراد البلوبرينت المركز لدائرة الإدارة

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
def dashboard():
    """
    مسار لوحة التحكم الرئيسية (مركز المراقبة).
    تم تعديل المسار ليقرأ dashboard.html مباشرة لحل خطأ TemplateNotFound.
    """
    # تصحيح: حذف 'admin/' لأن Flask يبحث الآن داخل مجلد templates المخصص للبلوبرينت
    return render_template('dashboard.html')

@admin_dashboard.route('/suppliers/list')
def list_suppliers():
    """
    مسار عرض سجل الموردين.
    يستخدم لتجنب خطأ BuildError عند النقر على روابط القائمة الجانبية.
    """
    return render_template('list_suppliers.html')
