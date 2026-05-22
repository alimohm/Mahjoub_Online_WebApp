# coding: utf-8
from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required
from apps import db 
from apps.models.wallet_db import SupplierWallet
from apps.models.supplier_db import Supplier
from sqlalchemy import func

# تأكد أن الاسم هنا 'wallet' ليطابق ما في __init__.py
wallet_bp = Blueprint('wallet', __name__, template_folder='templates')

@wallet_bp.route('/wallet_page')
@login_required
def wallet_home(): # قمنا بتغيير الاسم لـ wallet_home
    totals = db.session.query(
        func.sum(SupplierWallet.yer_total).label('total_yer'),
        func.sum(SupplierWallet.sar_total).label('total_sar'),
        func.sum(SupplierWallet.usd_total).label('total_usd')
    ).first()
    
    return render_template('admin/wallet_dashboard.html', totals=totals)

# ... بقية الدوال (يجب تغيير كل admin_wallet. إلى wallet.) ...
# مثال لتعديل دالة الإرجاع في نهاية adjust_balance:
# return redirect(url_for('wallet.wallet_home'))
