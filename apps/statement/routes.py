# coding: utf-8
from flask import render_template, request, jsonify
from flask_login import login_required
from apps.extensions import db
from apps.statement import statement_blueprint
from apps.models.supplier_db import Supplier
from apps.models.statement_db import SupplierStatement
from apps.models.wallet_db import SupplierWallet, WalletTransaction
from sqlalchemy import or_, func

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    currencies = ['USD', 'YER', 'SAR'] 
    return render_template('admin/statement.html', currencies=currencies)

# 1. البحث الذكي (يجب أن يعيد مفتاح "results" لـ Select2)
@statement_blueprint.route('/api/suppliers/search', methods=['GET'])
@login_required
def api_search_suppliers():
    term = request.args.get('q', '')
    suppliers = Supplier.query.filter(or_(
        Supplier.trade_name.ilike(f'%{term}%'),
        Supplier.sovereign_id.ilike(f'%{term}%'),
        Supplier.store_name.ilike(f'%{term}%'),
        Supplier.owner_name.ilike(f'%{term}%')
    )).limit(15).all()
    
    # تنسيق العرض للمستخدم في القائمة المنسدلة
    results = [
        {
            'id': s.id, 
            'text': f"{s.trade_name} | {s.store_name} | المالك: {s.owner_name} | الرقم: {s.sovereign_id}"
        } for s in suppliers
    ]
    return jsonify({"results": results})

# 2. جلب البيانات (تفصيلي + إجمالي)
@statement_blueprint.route('/api/statement/report', methods=['GET'])
@login_required
def api_get_report():
    s_id = request.args.get('id')
    curr = request.args.get('currency', 'ALL')
    start = request.args.get('start')
    end = request.args.get('end')

    supplier = Supplier.query.get(s_id)
    if not supplier: return jsonify({'error': 'المورد غير موجود'}), 404

    # أ. جلب كشف الحساب التفصيلي من SupplierStatement
    stmt_query = SupplierStatement.query.filter_by(supplier_id=supplier.id)
    if curr != 'ALL': stmt_query = stmt_query.filter_by(currency=curr)
    if start and end: stmt_query = stmt_query.filter(SupplierStatement.created_at.between(start, end))
    statements = stmt_query.order_by(SupplierStatement.created_at.desc()).all()

    # ب. جلب الأرباح من WalletTransaction عبر الربط بـ sovereign_id
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.sovereign_id).first()
    total_profit = 0
    if wallet:
        pq = WalletTransaction.query.filter_by(wallet_id=wallet.id)
        if curr != 'ALL': pq = pq.filter_by(currency=curr)
        if start and end: pq = pq.filter(WalletTransaction.created_at.between(start, end))
        total_profit = pq.with_entities(func.sum(WalletTransaction.profit_margin)).scalar() or 0

    return jsonify({
        'summary': {
            'total_debit': float(sum(s.debit for s in statements)),
            'total_credit': float(sum(s.credit for s in statements)),
            'net_balance': float(sum(s.credit for s in statements) - sum(s.debit for s in statements)),
            'total_profit': float(total_profit)
        },
        'details': [{
            'date': s.created_at.strftime('%Y-%m-%d %H:%M'),
            'desc': s.description or '---',
            'ref': s.reference_number or '---',
            'debit': float(s.debit),
            'credit': float(s.credit),
            'balance': float(s.running_balance)
        } for s in statements]
    })
