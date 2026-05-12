from flask import Blueprint, render_template, request, redirect, url_for, flash
from core.extensions import db
from core.models.supplier_db import Supplier

supplier_bp = Blueprint('supplier_app', __name__, template_folder='templates')

@supplier_bp.route('/suppliers')
def list_suppliers():
    # جلب جميع الموردين من قاعدة البيانات الجديدة
    all_suppliers = Supplier.query.order_by(Supplier.created_at.desc()).all()
    return render_template('supplier_list.html', suppliers=all_suppliers)
