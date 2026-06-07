from flask import render_template, request, jsonify
from apps.models.wallet_db import Wallet, Transaction, Supplier # تأكد من استيراد الموديلات
from sqlalchemy import func

# دالة عرض الداشبورد الرئيسية (تجمع الفلاتر والموردين)
@wallet_app.route('/wallet_dashboard')
def wallet_dashboard():
    # 1. حساب الفلاتر (الإحصائيات)
    stats = {
        "usd": db.session.query(func.sum(Wallet.balance_usd)).scalar() or 0,
        "sar": db.session.query(func.sum(Wallet.balance_sar)).scalar() or 0,
        "yer": db.session.query(func.sum(Wallet.balance_yer)).scalar() or 0,
        "count": Wallet.query.count()
    }
    return render_template('admin/wallet_app.html', stats=stats)

# دالة جلب قائمة الموردين مع التصفح (Pagination)
@wallet_app.route('/wallet/get_suppliers_list')
def get_suppliers_list():
    page = request.args.get('page', 1, type=int)
    # جلب الموردين 10 في كل صفحة
    pagination = Supplier.query.paginate(page=page, per_page=10)
    return render_template('admin/suppliers_list.html', suppliers=pagination)

# دالة البحث الذكي (API)
@wallet_app.route('/api/search')
def search_api():
    query = request.args.get('q', '')
    suppliers = Supplier.query.filter(Supplier.trade_name.ilike(f'%{query}%')).limit(10).all()
    results = [{"id": s.id, "text": s.trade_name} for s in suppliers]
    return jsonify({"results": results})
