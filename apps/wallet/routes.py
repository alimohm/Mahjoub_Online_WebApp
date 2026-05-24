# coding: utf-8
import os
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models.wallet_db import SupplierWallet
from apps.models.settlements_db import AdminSettlement # تأكد من استيراد الموديل الصحيح
from datetime import datetime

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
wallet_blueprint = Blueprint('wallet', __name__, template_folder=template_dir)

@wallet_blueprint.route('/management', methods=['GET'])
@login_required
def display_management_table():
    search_query = request.args.get('search_query', '')
    wallet = None
    wallet_settlements = []
    # ملاحظة: إذا كان لديك جدول منفصل للسحب المعلق، استبدله هنا
    pending_withdrawals = [] 

    total_wallets_count = SupplierWallet.query.count()
    total_yer_system = db.session.query(db.func.sum(SupplierWallet.yer_total)).scalar() or 0
    total_sar_system = db.session.query(db.func.sum(SupplierWallet.sar_total)).scalar() or 0
    total_usd_system = db.session.query(db.func.sum(SupplierWallet.usd_total)).scalar() or 0

    if search_query:
        wallet = SupplierWallet.query.filter(
            (SupplierWallet.supplier_id == search_query) | 
            (SupplierWallet.wallet_code == search_query)
        ).first()
        
        if wallet:
            # استعلام التسويات من جدول AdminSettlement الذي أرسلته
            wallet_settlements = AdminSettlement.query.filter_by(wallet_id=wallet.id)\
                .order_by(AdminSettlement.created_at.desc()).all()

    try:
        return render_template('admin/settlement_and_withdrawal.html',
                               total_wallets_count=total_wallets_count,
                               total_yer_system=total_yer_system,
                               total_sar_system=total_sar_system,
                               total_usd_system=total_usd_system,
                               wallet=wallet,
                               wallet_settlements=wallet_settlements,
                               pending_withdrawals=pending_withdrawals,
                               current_search=search_query)
    except Exception as e:
        return f"Error: {str(e)}", 500

@wallet_blueprint.route('/execute-settlement/<wallet_code>', methods=['POST'])
@login_required
def execute_admin_settlement(wallet_code):
    wallet = SupplierWallet.query.filter_by(wallet_code=wallet_code).first_or_404()
    
    # إنشاء قيد جديد في AdminSettlement
    new_settlement = AdminSettlement(
        wallet_id=wallet.id,
        wallet_code=wallet.wallet_code,
        settlement_code=AdminSettlement.generate_settlement_code(),
        settlement_type=request.form.get('settlement_type'),
        currency=request.form.get('currency'),
        amount=float(request.form.get('amount', 0)),
        financial_entity=request.form.get('financial_entity'),
        reference_number=request.form.get('reference_number'),
        reason_notes=request.form.get('notes'),
        created_by=current_user.username if hasattr(current_user, 'username') else 'Admin'
    )
    
    # تحديث رصيد المحفظة هنا بنفس المنطق السابق...
    db.session.add(new_settlement)
    db.session.commit()
    flash("تم اعتماد سند التسوية بنجاح", "success")
    return redirect(url_for('wallet.display_management_table', search_query=wallet_code))
