from flask import render_template
from . import admin_dashboard  # استيراد البلوبرينت الذي أنشأناه في __init__

@admin_dashboard.route('/')
@admin_dashboard.route('/dashboard')
def dashboard():
    # هذا سيجعل الهيكل والديشبورد يعملان معاً
    return render_template('admin/dashboard.html')

# أضفنا هذا المسار لمنع خطأ BuildError الذي ظهر سابقاً
@admin_dashboard.route('/suppliers/list')
def list_suppliers():
    return render_template('admin/list_suppliers.html')
