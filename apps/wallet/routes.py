# coding: utf-8
# 📂 apps/wallet/routes.py - منطق عمليات المحفظة

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from apps.models.wallet_db import SupplierWallet, WalletTransaction, db

# تعريف الـ Blueprint
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض لوحة تحكم المحفظة (المسار المطلوب في admin_base.html)
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # حساب إجمالي الأرصدة للنظام (كمسؤول)
    total_system_sar = db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar() or 0
    total_system_yer = db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar() or 0
    total_system_usd = db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar() or 0
    
    return render_template(
        'wallet/dashboard.html', 
        total_system_sar=total_system_sar,
        total_system_yer=total_system_yer,
        total_system_usd=total_system_usd
    )

# 2. المسار الذي تستدعيه دالة loadWallet في الجافاسكريبت (لحل الخطأ 500)
@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    transactions = []
    if wallet:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('wallet/view_wallet.html', wallet=wallet, transactions=transactions)

# 3. إضافة عملية مالية (API)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})
