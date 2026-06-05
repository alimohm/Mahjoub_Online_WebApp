# coding: utf-8
# 📂 apps/wallet/routes.py - منطق عمليات المحفظة

from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import login_required, current_user
from apps.extensions import db
from .models import SupplierWallet, WalletTransaction # تأكد من أنك تستورد النماذج من مكانها الصحيح

# تعريف الـ Blueprint الخاص بالمحفظة
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. # coding: utf-8
# 📂 apps/wallet/routes.py - منطق عمليات المحفظة (النسخة المستقرة)

from flask import Blueprint, render_template, jsonify
from flask_login import login_required, current_user
from apps.extensions import db

# استيراد النماذج من المسار الصحيح والموحد (apps.models)
from apps.models.wallet_db import SupplierWallet, WalletTransaction

# تعريف الـ Blueprint الخاص بالمحفظة
# template_folder='templates' تعني أن Flask سيبحث عن ملفات HTML داخل apps/wallet/templates
wallet_app = Blueprint(
    'wallet_app', 
    __name__, 
    template_folder='templates'
)

# 1. عرض لوحة تحكم المحفظة
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # جلب محفظة المورد الحالي
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    
    # جلب المعاملات الخاصة بهذه المحفظة
    transactions = []
    if wallet:
        transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id)\
            .order_by(WalletTransaction.created_at.desc()).all()
    
    return render_template('wallet/dashboard.html', wallet=wallet, transactions=transactions)

# 2. مثال لمسار بيانات (API) لإضافة عملية مالية
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    # هنا سيتم إضافة المنطق الخاص بإضافة العمليات المالية
    return jsonify({"status": "success", "message": "تمت إضافة العملية بنجاح"})

# لا تقم بوضع app.run() أو أي استيراد للمصنع الرئيسي هنا!
# هذا الملف يعمل كجزء مستقل يتم ربطه بواسطة المصنع.عرض محفظة المورد
@wallet_app.route('/dashboard')
@login_required
def wallet_dashboard():
    # هنا جلب بيانات المحفظة الخاصة بالمورد الحالي
    wallet = SupplierWallet.query.filter_by(supplier_id=current_user.id).first()
    transactions = WalletTransaction.query.filter_by(wallet_id=wallet.id).order_by(WalletTransaction.created_at.desc()).all() if wallet else []
    
    return render_template('wallet/dashboard.html', wallet=wallet, transactions=transactions)

# 2. إضافة عملية مالية (مثال على مسار داخلي)
@wallet_app.route('/add_transaction', methods=['POST'])
@login_required
def add_transaction():
    # منطق إضافة عملية مالية
    # ...
    return jsonify({"status": "success", "message": "تمت العملية بنجاح"})

# 3. أي مسارات أخرى خاصة بالمحفظة
# @wallet_app.route('/withdraw', ...)
# ...
