# تأكد من أن دالة الداشبورد في routes.py تقوم بالتالي:
@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    # هنا تقوم بجلب البيانات من قاعدة البيانات
    totals = {
        'total_yer': 1500000, # استبدل هذه بقيمة حقيقية من DB
        'total_sar': 50000,
        'total_usd': 12000
    }
    
    # التحقق من أن الطلب هو AJAX
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return render_template('admin/dashboard_content.html', totals=totals)
    
    return render_template('admin/admin_base.html')
