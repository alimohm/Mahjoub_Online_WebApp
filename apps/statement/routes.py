# كود مقترح لتحديث المسار (JSON API)
@statement_blueprint.route('/statement/get_data', methods=['GET'])
@login_required
def get_statement_data():
    supplier_id = request.args.get('id')
    # 1. جلب بيانات المورد
    supplier = Supplier.query.get(supplier_id)
    # 2. جلب الكشوفات
    statements = SupplierStatement.query.filter_by(supplier_id=supplier_id).all()
    # 3. جلب بيانات المحفظة (للحصول على الأرصدة الحالية والأرباح)
    wallet = SupplierWallet.query.filter_by(supplier_id=supplier.sovereign_id).first()
    
    return jsonify({
        'supplier': supplier.to_dict(),
        'wallet': {
            'yer': wallet.yer_total,
            'sar': wallet.sar_total,
            'usd': wallet.usd_total
        },
        'statements': [s.to_dict() for s in statements],
        'total_profit': sum(t.profit_margin for t in wallet.transactions) # مجموع الأرباح
    })
