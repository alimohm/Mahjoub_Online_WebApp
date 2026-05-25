# coding: utf-8
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required
from apps import db
from apps.models import Wallet, Supplier, WithdrawalRequest
from apps.models.settlements_db import AdminSettlement

# تعريف البلوبرينت
wallet_blueprint = Blueprint('wallet', __name__)

@wallet_blueprint.route('/management', methods=['GET'])
@login_required
def display_management_table():
    search_query = request.args.get('search_query')
    wallet = None
    pending_withdrawals = []
    settlements = []
    
    # إحصائيات النظام العامة
    total_wallets_count = Wallet.query.count()
    total_yer_system = db.session.query(db.func.sum(Wallet.yer_available)).scalar() or 0
    total_sar_system = db.session.query(db.func.sum(Wallet.sar_available)).scalar() or 0
    
    if search_query:
        # البحث الشامل في المحافظ ومرتبطاتها
        wallet = Wallet.query.join(Supplier).filter(
            (Wallet.wallet_code.ilike(f'%{search_query}%')) |
            (Wallet.supplier_id.ilike(f'%{search_query}%')) |
            (Supplier.name.ilike(f'%{search_query}%')) |
            (Supplier.owner_name.ilike(f'%{search_query}%'))
        ).first()
        
        if wallet:
            # جلب طلبات السحب المعلقة للتبويب الأول
            pending_withdrawals = WithdrawalRequest.query.filter_by(
                wallet_id=wallet.id, status='pending'
            ).all()
            
            # جلب سندات التسوية من الجدول المخصص للتبويب الثاني
            settlements = AdminSettlement.query.filter_by(
                wallet_id=wallet.id
            ).order_by(AdminSettlement.created_at.desc()).all()
    
    return render_template(
        'admin/settlement_and_withdrawal.html',
        wallet=wallet,
        pending_withdrawals=pending_withdrawals,
        settlements=settlements,
        total_wallets_count=total_wallets_count,
        total_yer_system=total_yer_system,
        total_sar_system=total_sar_system,
        current_search=search_query
    )

@wallet_blueprint.route('/withdrawal/handle/<int:tx_id>/<decision>', methods=['POST'])
@login_required
def handle_supplier_withdrawal(tx_id, decision):
    request_obj = WithdrawalRequest.query.get_or_404(tx_id)
    
    if decision == 'approve':
        request_obj.status = 'approved'
        flash("تم اعتماد طلب السحب بنجاح", "success")
    else:
        request_obj.status = 'rejected'
        flash("تم رفض طلب السحب", "danger")
        
    db.session.commit()
    # العودة إلى صفحة الإدارة مع الحفاظ على البحث الحالي
    return redirect(url_for('wallet.display_management_table', search_query=request_obj.wallet.wallet_code))
