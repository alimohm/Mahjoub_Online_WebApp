# coding: utf-8
# 🔑 محرك العمليات المالية والتحكم بالمحافظ - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from apps import db
from apps.models.wallet_db import Wallet, WalletTransaction
from apps.models.supplier_db import Supplier  # استدعاء موديل المورد للفحص الحوكمي المباشر
from . import admin_wallet  # استيراد البلوبرينت الخاص بإدارة المحفظة
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func
from sqlalchemy import or_

@admin_wallet.route('/overview', methods=['GET'])
@login_required
def overview():
    """
    الواجهة السيادية الموحدة لإدارة وحوكمة المحافظ المالية للإدارة العليا.
    مؤمنة بالكامل ضد حقول التداخل البرمجي القاتلة N+1 عبر التحميل المسبق.
    """
    try:
        # 1. احتساب المؤشرات المالية الكلية للمنصة (الريال اليمني) مع معالجة القيم الفارغة
        yer_totals = db.session.query(
            func.coalesce(func.sum(Wallet.yer_total), 0.0),
            func.coalesce(func.sum(Wallet.yer_available), 0.0),
            func.coalesce(func.sum(Wallet.yer_pending), 0.0)
        ).first()

        # 2. احتساب المؤشرات المالية الكلية للمنصة (الريال السعودي) مع معالجة القيم الفارغة
        sar_totals = db.session.query(
            func.coalesce(func.sum(Wallet.sar_total), 0.0),
            func.coalesce(func.sum(Wallet.sar_available), 0.0),
            func.coalesce(func.sum(Wallet.sar_pending), 0.0)
        ).first()

        # 3. احتساب المؤشرات المالية الكلية للمنصة (الدولار الأمريكي) مع معالجة القيم الفارغة
        usd_totals = db.session.query(
            func.coalesce(func.sum(Wallet.usd_total), 0.0),
            func.coalesce(func.sum(Wallet.usd_available), 0.0),
            func.coalesce(func.sum(Wallet.usd_pending), 0.0)
        ).first()

        # 4. جلب طلبات السحب المعلقة (Pending) مع تحميل متسلسل آمن للمحفظة لمنع البطء
        pending_withdrawals = db.session.query(WalletTransaction)\
            .options(joinedload(WalletTransaction.wallet))\
            .filter(WalletTransaction.tx_type == 'withdrawal', WalletTransaction.tx_status == 'pending')\
            .order_by(WalletTransaction.created_at.desc())\
            .all()

        # تجميع المؤشرات المالية في قاموس منظم ومضمون القيمة لمنع أخطاء جينجا القاتلة
        platform_metrics = {
            "YER": {"total": yer_totals[0] or 0.0, "available": yer_totals[1] or 0.0, "pending": yer_totals[2] or 0.0},
            "SAR": {"total": sar_totals[0] or 0.0, "available": sar_totals[1] or 0.0, "pending": sar_totals[2] or 0.0},
            "USD": {"total": usd_totals[0] or 0.0, "available": usd_totals[1] or 0.0, "pending": usd_totals[2] or 0.0}
        }

        return render_template(
            'admin/overview.html',
            metrics=platform_metrics,
            pending_tx=pending_withdrawals,
            owner=current_user
        )

    except Exception as e:
        current_app.logger.error(f"❌ خطأ حوكمي أثناء تشغيل واجهة المحافظ: {str(e)}")
        return f"<h3>خطأ مالي في السيرفر الداخلي للعملات:</h3> <p>{str(e)}</p>", 500


@admin_wallet.route('/api/search', methods=['GET'])
@login_required
def search_wallets():
    """
    نظام استدعاء المحافظ السيادي المباشر:
    يبحث عن الموردين بالاسم أو رقم الهاتف، ويستخراج المحفظة الحية الخاصة بهم 
    مع أرصدة العملات الثلاث (YER, SAR, USD) للتفاعل الفوري مع الواجهة عبر AJAX.
    """
    query = request.args.get('query', '').strip()
    if not query:
        return jsonify({'status': 'success', 'wallets': []})

    try:
        # فحص الموردين المطابقين للاسم أو الهاتف في قاعدة البيانات
        suppliers = db.session.query(Supplier).filter(
            or_(
                Supplier.username.ilike(f'%{query}%'),
                Supplier.phone.ilike(f'%{query}%')
            )
        ).all()

        wallets_list = []
        for sup in suppliers:
            # استدعاء المحفظة المرتبطة بالمورد المباشر عبر المعرف الفريد
            wallet = db.session.query(Wallet).filter(Wallet.supplier_id == sup.id).first()
            
            # حماية البيانات وإرجاع قيم صفرية افتراضية في حال عدم تأسيس المحفظة مسبقاً
            wallets_list.append({
                'wallet_id': wallet.id if wallet else f"⏳ مفقودة (ID: {sup.id})",
                'trade_name': sup.username,  
                'sovereign_id': f"SUP-ID-{sup.id:04d}",
                'owner_phone': sup.phone or "بدون هاتف",
                
                # كشوفات الريال اليمني
                'yer_total': float(wallet.yer_total) if wallet else 0.0,
                'yer_available': float(wallet.yer_available) if wallet else 0.0,
                'yer_pending': float(wallet.yer_pending) if wallet else 0.0,
                
                # كشوفات الريال السعودي
                'sar_total': float(wallet.sar_total) if wallet else 0.0,
                'sar_available': float(wallet.sar_available) if wallet else 0.0,
                'sar_pending': float(wallet.sar_pending) if wallet else 0.0,
                
                # كشوفات الدولار الأمريكي
                'usd_total': float(wallet.usd_total) if wallet else 0.0,
                'usd_available': float(wallet.usd_available) if wallet else 0.0,
                'usd_pending': float(wallet.usd_pending) if wallet else 0.0,
            })

        return jsonify({'status': 'success', 'wallets': wallets_list})

    except Exception as e:
        current_app.logger.error(f"❌ خطأ أثناء استدعاء بيانات المحافظ: {str(e)}")
        return jsonify({'status': 'error', 'message': str(e)}), 500


@admin_wallet.route('/approve-withdrawal', methods=['POST'])
@login_required
def approve_withdrawal():
    """
    محرك التعميد المالي السيادي: الموافقة على طلب السحب وتحويل الأموال للمورد.
    يستخدم الحظر الصارم (with_for_update) لمنع ثغرات تضارب السجلات Race Condition.
    """
    tx_id = request.form.get('tx_id')
    if not tx_id:
        return jsonify({"status": "error", "message": "المعرف الفريد للعملية مفقود."}), 400

    try:
        # استخدام with_for_update لحظر تضارب السجلات على السيرفر الحي
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير موجودة أو تم تعميدها مسبقاً."}), 400

        wallet = Wallet.query.with_for_update().get(transaction.wallet_id)
        currency = transaction.currency
        amount = transaction.amount

        # الخصم المالي الحوكمي وتعديل الأرصدة الكلية بالتوازي مع تفريغ الحقل المعلق
        if currency == 'YER':
            if wallet.yer_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الريال اليمني المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.yer_pending -= amount
            wallet.yer_total -= amount
            wallet.yer_withdrawn += amount
            
        elif currency == 'SAR':
            if wallet.sar_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الريال السعودي المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.sar_pending -= amount
            wallet.sar_total -= amount
            wallet.sar_withdrawn += amount
            
        elif currency == 'USD':
            if wallet.usd_pending < amount:
                return jsonify({"status": "error", "message": "رصيد الدولار المعلق غير كافٍ لإتمام العملية."}), 400
            wallet.usd_pending -= amount
            wallet.usd_total -= amount
            wallet.usd_withdrawn += amount

        # تحديث حالة السجل المالي وتوثيق هوية الإداري المعمّد للعملية
        transaction.tx_status = 'completed'
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تعميد صرف الحوالة بنجاح برقم المرجع: {transaction.transaction_ref}"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطر مالي أثناء تعميد السحب: {str(e)}")
        return jsonify({"status": "error", "message": f"فشل التعميد المالي: {str(e)}"}), 500


@admin_wallet.route('/reject-withdrawal', methods=['POST'])
@login_required
def reject_withdrawal():
    """
    رفض طلب السحب سيادياً: إعادة الأموال المحتجزة من الرصيد المعلق (Pending) إلى رصيد المورد المتاح (Available).
    """
    tx_id = request.form.get('tx_id')
    reason = request.form.get('reason', 'تم الرفض من قبل الإدارة العليا').strip()

    if not tx_id:
        return jsonify({"status": "error", "message": "المعرف الفريد للعملية مفقود."}), 400

    try:
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير صالحة لإجراء الرفض."}), 400

        wallet = Wallet.query.with_for_update().get(transaction.wallet_id)
        currency = transaction.currency
        amount = transaction.amount

        # إعادة فك الحجز المالي: تحويل الرصيد من المعلق إلى المتاح مجدداً
        if currency == 'YER':
            wallet.yer_pending -= amount
            wallet.yer_available += amount
        elif currency == 'SAR':
            wallet.sar_pending -= amount
            wallet.sar_available += amount
        elif currency == 'USD':
            wallet.usd_pending -= amount
            wallet.usd_available += amount

        # إسقاط الحوالة برمجياً وتوثيق مبرر الرفض للأرشيف الإداري والتجاري
        transaction.tx_status = 'rejected'
        transaction.description = f"{transaction.description} | سبب الرفض الحوكمي: {reason}"
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": "تم رفض طلب السحب بنجاح وإعادة فك حجز الأموال إلى رصيد التاجر المتاح."}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطأ أثناء إسقاط العملية المالية: {str(e)}")
        return jsonify({"status": "error", "message": f"فشل إجراء إسقاط الحوالة: {str(e)}"}), 500
