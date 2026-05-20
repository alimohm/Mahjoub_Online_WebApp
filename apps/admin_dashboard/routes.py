# coding: utf-8
# ⚙️ محرك لوحة التحكم السيادية - منصة محجوب أونلاين 2026

from flask import render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from . import admin_dashboard
from apps.models.supplier_db import Supplier

@admin_dashboard.route('/dashboard', methods=['GET'])
@login_required
def dashboard_home():
    """
    عرض لوحة القيادة (Dashboard) الرئيسية.
    """
    try:
        # إحصائية بسيطة لشركاء النجاح
        total_suppliers = Supplier.query.count()
        stats = {
            'total_suppliers': total_suppliers,
            'system_health': '100% مستقر'
