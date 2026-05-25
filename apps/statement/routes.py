# coding: utf-8
# 📂 apps/statement/routes.py
# ⚙️ محرك كشوفات الموردين المركزية - نظام محجوب أونلاين 2026

from flask import render_template, request, flash
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.utils.report_generator import ReportGenerator
from sqlalchemy import or_

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    """
    محرك عرض كشف حساب الموردين.
    تم نقل استيراد Supplier إلى هنا لكسر حلقة الاستيراد الدائرية.
    """
    from apps.models.supplier_db import Supplier
    
    # 1. التقاط مدخلات البحث والفلترة
    q = request.args.get('q', '')
    currency = request.args.get('currency', 'ALL')
    report_type = request.args.get('report_type', 'detailed')
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')
    
    selected_supplier = None
    statements = []

    # 2. منطق البحث الذكي
    if q
