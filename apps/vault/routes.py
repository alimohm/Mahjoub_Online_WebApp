# coding: utf-8
# 📂 apps/vault/routes.py - مسارات الخزينة المركزية

from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.extensions import db
from apps.models.vault_db import AdminVault, VaultTransaction

vault_bp = Blueprint('vault_bp', __name__, template_folder='templates')

@vault_bp.route('/admin/vault', methods=['GET'])
@login_required
def vault_dashboard():
    # استرجاع الخزينة (أو إنشاؤها إذا لم توجد)
    vault = AdminVault.query.first()
    if not vault:
        # تأمين أولي للخزينة عند أول دخول
        vault = AdminVault(balance_sar=0.0, balance_yer=0.0, balance_usd=0.0)
        db.session.add(vault)
        db.session.commit()
    
    # استرجاع آخر 20 عملية
    transactions = VaultTransaction.query.order_by(VaultTransaction.created_at.desc()).limit(20).all()
    
    return render_template(
        'admin/vault_dashboard.html', 
        vault=vault, 
        transactions=transactions
    )

@vault_bp.route('/admin/vault/verify', methods=['POST'])
@login_required
def verify_integrity():
    """التحقق من سلامة البيانات ومطابقة الـ Hash"""
    vault = AdminVault.query.first()
    if vault and vault.integrity_hash:
        if vault.generate_integrity_hash() == vault.integrity_hash:
            flash("✅ سلامة بيانات الخزينة مؤكدة ومطابقة.", "success")
        else:
            flash("⚠️ تحذير: تم اكتشاف تلاعب في سجلات الخزينة!", "danger")
    return redirect(url_for('vault_bp.vault_dashboard'))
