# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.admin_dashboard import admin_dashboard_bp

def get_totals():
    # استبدل هذه القيم باستعلامات قاعدة البيانات الحقيقية
    return {
        'total_yer': 1500000.00,
        'total_sar': 5000.00,
        'total_usd': 1200.00
    }

@admin_dashboard_bp.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    # التحقق مما إذا كان الطلب قادماً من محرك AJAX
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    
    # إذا كان الطلب داخلياً، أ
