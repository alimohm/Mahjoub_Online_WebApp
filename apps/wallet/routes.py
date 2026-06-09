# 📂 apps/wallet/routes.py
from flask import Blueprint, render_template, request, jsonify
from apps.extensions import db
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from apps.models.supplier_db import Supplier
from flask_login import login_required

# تعريف الـ Blueprint باسم wallet_app ليطابق ما في __init__.py
wallet_app = Blueprint('wallet_app', __name__)

@wallet_app.route('/dashboard')
@login_required
def dashboard():
    search_query = request.args.get('search', '')
    
    # بناء الاستعلام لجلب المحافظ مع بيانات المورد المرتبطة بها
    query = SupplierWallet.query.join(Supplier)
    
    if search_query:
        query = query.filter(
            (Supplier.trade_name.contains(search_query)) | 
            (Supplier.owner_name.contains(search_query)) |
            (Supplier.owner_phone.contains(search_query))
        )
    
    wallets = query.all()
    
    return render_template('admin/wallet_app.html', wallets=wallets)

@wallet_app.route('/view/<int:supplier_id>')
@login_required
def view_wallet(supplier_id):
    # جلب المحفظة الخاصة بالمورد
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier_id).first_or_404()
    
    # جلب العمليات الخاصة بهذه المحفظة
    transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
        .order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('admin/view_wallet.html', 
                           wallet=wallet, 
                           transactions=transactions)

@wallet_app.route('/api/search')
@login_required
def search_suppliers():
    query = request.args.get('q', '')
    suppliers = Supplier.query.filter(
        (Supplier.trade_name.contains(query)) | 
        (Supplier.owner_phone.contains(query))
    ).limit(10).all()
    
    return jsonify({
        'results': [{'id': s.id, 'name': s.trade_name, 'phone': s.owner_phone} for s in suppliers]
    })
