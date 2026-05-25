# coding: utf-8
from flask import render_template, request
from flask_login import login_required
from apps.statement import statement_blueprint
from apps.models.statement_db import SupplierStatement
from apps.models.supplier_db import Supplier

@statement_blueprint.route('/view', methods=['GET'])
@login_required
def view_statement():
    # 1. تنظيف المدخلات بشكل آمن
    raw_supplier_id = request.args.get('supplier_id')
    supplier_id = None
    if raw_supplier_id and raw_supplier_id.isdigit():
        supplier_id = int(raw_supplier_id)
    
    all_suppliers = Supplier.query.order_by(Supplier.trade_name.asc()).all()
    statements = []
    supplier = None
    balances = {'SAR': 0.0, 'YER': 0.0, 'USD': 0.0}

    # 2. جلب البيانات فقط إذا كان الـ ID صالحاً
    if supplier_id:
        supplier = Supplier.query.get(supplier_id)
        if supplier:
            statements = SupplierStatement.query.filter_by(supplier_id=supplier_id)\
                                               .order_by(SupplierStatement.created_at.desc()).all()
            
            # 3. حساب الأرصدة مع معالجة آمنة للقيم الفارغة
            for stmt in statements:
                # التأكد من وجود العملة في القاموس
                currency = stmt.currency
                if currency in balances:
                    # تحويل القيم لـ float بأمان (معالجة None إلى 0.0)
                    credit = float(stmt.credit) if stmt.credit is not None else 0.0
                    debit = float(stmt.debit) if stmt.debit is not None else 0.0
                    balances[currency] += (credit - debit)

    return render_template('admin/statement.html', 
                           statements=statements,
                           all_suppliers=all_suppliers,
                           selected_supplier=supplier,
                           balances=balances)
