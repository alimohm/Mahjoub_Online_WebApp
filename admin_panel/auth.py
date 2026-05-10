from flask import render_template, request, flash, redirect, url_for
from .auth_logic import AdminAuthLogic

def login_view():
    """
    محرك العرض (View Engine):
    هذه هي الدالة التي يستدعيها السيرفر عند زيارة رابط /admin/login
    """
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # استدعاء المنطق السيادي الذي كتبته أنت في AdminAuthLogic
        success, message, user = AdminAuthLogic.authenticate_admin(username, password)
        
        if success:
            # تم الدخول بنجاح
            return redirect(url_for('admin.dashboard'))
        else:
            # فشل الدخول - إظهار رسالة الخطأ السيادية
            flash(message, 'danger')
            
    # عرض واجهة الدخول الملكية (قالب HTML)
    return render_template('admin/login.html')
