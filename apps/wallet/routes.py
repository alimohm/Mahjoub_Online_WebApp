# 📂 apps/wallet/routes.py
from flask import Blueprint, render_template, jsonify
from flask_login import login_required
from sqlalchemy import func
from apps.extensions import db  # تأكد من مسار الـ db لديك
from apps.models.supplier_db import Supplier
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# --- هذا هو السطر الحاسم ---
# يجب أن يكون اسم المتغير هنا 'wallet_app' 
# ليطابق الاستدعاء في __init__.py
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.id).first()
    transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
                    .order_by(WalletTransaction.created_at.desc())\
                    .limit(50).all()
    
    return render_template('admin/wallet_app.html', 
                           supplier=supplier, 
                           wallet=wallet, 
                           transactions=transactions)

@wallet_app.route('/api/stats')
@login_required
def get_stats():
    totals = db.session.query(
        func.sum(SupplierWallet.balance_sar),
        func.sum(SupplierWallet.balance_yer),
        func.sum(SupplierWallet.balance_usd)
    ).first()
    
    return jsonify({
        'sar': float(totals[0] or 0),
        'yer': float(totals[1] or 0),
        'usd': float(totals[2] or 0)
    })
