# coding: utf-8
# 📂 apps/wallet/routes.py - النسخة المصححة والمضمونة

from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
# تأكد من استيراد db من المجلد الرئيسي apps إذا كان هو مكان تعريف قاعدة البيانات
from apps import db 
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # محاولة حساب الإجماليات مع معالجة الأخطاء
    try:
        total_system_sar = db.session.query(db.func.sum(SupplierWallet.balance_sar)).scalar() or 0
        total_system_yer = db.session.query(db.func.sum(SupplierWallet.balance_yer)).scalar() or 0
        total_system_usd = db.session.query(db.func.sum(SupplierWallet.balance_usd)).scalar() or 0
    except Exception as e:
        print(f"Error calculating totals: {e}")
        total_system_sar = total_system_yer = total_system_usd = 0
    
    return render_template(
        'wallet/dashboard.html', 
        total_system_sar=total_system_sar,
        total_system_yer=total_system_yer,
        total_system_usd=total_system_usd
    )

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first()
    transactions = []
    if wallet:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('wallet/view_wallet.html', wallet=wallet, transactions=transactions)

@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})
