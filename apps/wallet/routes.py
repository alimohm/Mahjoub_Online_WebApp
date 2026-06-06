# coding: utf-8
# 📂 apps/wallet/routes.py - منطق عمليات المحفظة (النسخة النهائية والمصححة)

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint
# الاسم 'wallet_app' هو الذي سيُستخدم في url_for
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض لوحة تحكم المحفظة
# المسار الكامل هو /wallet/dashboard
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # جلب محفظة المورد الحالي
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    
    # جلب المعاملات مرتبة حسب الأحدث
    transactions = []
    if wallet:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).all()
    
    # القالب يجب أن يكون موجوداً في apps/wallet/templates/wallet/dashboard.html
    return render_template('wallet/dashboard.html', wallet=wallet, transactions=transactions)

# 2. إضافة عملية مالية (API)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    # منطق إضافة عملية مالية هنا
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})
