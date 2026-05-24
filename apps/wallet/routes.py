from flask import Blueprint, render_template, request, flash, redirect, url_for
from apps.models import db, Wallet, Settlement, WithdrawalRequest, Supplier
from flask_login import login_required, current_user

blueprint = Blueprint('wallet', __name__, url_prefix='/wallet')

@blueprint.route('/management', methods=['GET'])
@login_required
def display_management_table():
    search_query = request.args.get('search_query')
    wallet = None
    wallet_settlements = []
    
    # إحصائيات النظام العامة
    total_wallets_count = Wallet.query.count()
    total_yer_system = db.session.query(db.func.sum(Wallet.yer_available)).scalar() or 0
    total_sar_system = db.session.query(db.func.sum(Wallet.sar_available)).scalar() or 0
    
    if search_query:
        # البحث الشامل في المحافظ ومرتبطاتها (الموردين)
        # نستخدم join لجلب بيانات المورد ليتم عرضها في الواجهة
        wallet = Wallet.query.join(Supplier).filter(
            (Wallet.wallet_code.ilike(f'%{search_query}%')) |
            (Wallet.supplier_id.ilike(f'%{search_query}%')) |
            (Supplier.name.ilike(f'%{search_query}%')) |
            (Supplier.owner_name.ilike(f'%{search_query}%'))
        ).first()
        
        if wallet:
            # دمج سجلات التسويات وطلبات السحب (يمكنك إنشاء View أو دمجها برمجياً)
            # هنا نقوم بجلب التسويات كمثال
            wallet_settlements = Settlement.query.filter_by(wallet_id=wallet.id).order_by(Settlement.created_at.desc()).all()
            # إذا كنت تريد إضافة طلبات السحب لنفس الجدول، يمكنك جلبها هنا أيضاً
            # withdrawals = WithdrawalRequest.query.filter_by(wallet_id=wallet.id).all()
    
    return render_template('admin/settlement_and_withdrawal.html',
                           wallet=wallet,
                           wallet_settlements=wallet_settlements,
                           total_wallets_count=total_wallets_count,
                           total_yer_system=total_yer_system,
                           total_sar_system=total_sar_system,
                           current_search=search_query)

@blueprint.route('/withdrawal/handle/<int:tx_id>/<decision>', methods=['POST'])
@login_required
def handle_supplier_withdrawal(tx_id, decision):
    # مسار معالجة طلبات السحب
    request_obj = WithdrawalRequest.query.get_or_404(tx_id)
    
    if decision == 'approve':
        request_obj.status = 'approved'
        flash("تم اعتماد طلب السحب بنجاح", "success")
    else:
        request_obj.status = 'rejected'
        flash("تم رفض طلب السحب", "danger")
        
    db.session.commit()
    return redirect(url_for('wallet.display_management_table', search_query=request_obj.wallet.wallet_code))
