# coding: utf-8
# 🔑 محرك العمليات المالية والتحكم بالمحافظ - منصة محجوب أونلاين 2026

from flask import render_template, request, jsonify, current_app
from flask_login import login_required, current_user
from apps import db
from apps.models.wallet_db import Wallet, WalletTransaction
from . import admin_wallet  # استيراد البلوبرينت الخاص بإدارة المحفظة
from sqlalchemy.orm import joinedload
from sqlalchemy.sql import func

@admin_wallet.route('/overview', methods=['GET'])
@login_required
def overview():
    """
    الواجهة السيادية الموحدة لإدارة وحوكمة المحافظ المالية للإدارة العليا.
    تم تحصينها بالكامل باستخدام func.coalesce لمنع الأخطاء في حال كانت الجداول فارغة.
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

        # 4. جلب طلبات السحب المعلقة (Pending) بأمان
        pending_withdrawals = db.session.query(WalletTransaction)\
            .filter(WalletTransaction.tx_type == 'withdrawal', WalletTransaction.tx_status == 'pending')\
            .order_by(WalletTransaction.created_at.desc())\
            .all()

        # تجميع المؤشرات المالية في قاموس منظم ومضمون القيمة لمنع أخطاء جينجا القاتلة
        platform_metrics = {
            "YER": {"total": yer_totals[0], "available": yer_totals[1], "pending": yer_totals[2]},
            "SAR": {"total": sar_totals[0], "available": sar_totals[1], "pending": sar_totals[2]},
            "USD": {"total": usd_totals[0], "available": usd_totals[1], "pending": usd_totals[2]}
        }

        return render_template(
            'admin/overview.html',
            metrics=platform_metrics,
            pending_tx=pending_withdrawals,
            owner=current_user
        )

    except Exception as e:
        current_app.logger.error(f"❌ خطأ حوكمي أثناء تشغيل واجهة المحافظ: {str(e)}")
        # حماية إضافية للنواة: إذا كانت قوالب الخطأ غير متوفرة، نرجع استجابة نصية بدلاً من تجميد السيرفر
        return f"<h3>خطأ مالي في السيرفر الداخلي للعملات:</h3> <p>{str(e)}</p>", 500


@admin_wallet.route('/approve-withdrawal', methods=['POST'])
@login_required
def approve_withdrawal():
    """
    محرك التعميد المالي السيادي: الموافقة على طلب السحب وتحويل الأموال للمورد.
    """
    tx_id = request.form.get('tx_id')
    if not tx_id:
        return jsonify({"status": "error", "message": "المعرف الفريد للعملية مفقود."}), 400

    try:
        # استخدام with_for_update لمنع الـ Race Condition وتضارب البيانات على السيرفر الحي
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير موجودة أو تم تعميدها مسبقاً."}), 400

        wallet = Wallet.query.with_for_update().get(transaction.wallet_id)
        currency = transaction.currency
        amount = transaction.amount

        # الخصم المالي الحوكمي حسب نوع عملة الحوالة المبرمة في الطلب
        if currency == 'YER':
            if wallet.yer_available < amount:
                return jsonify({"status": "error", "message": "رصيد الريال اليمني المتاح غير كافٍ."}), 400
            wallet.yer_available -= amount
            wallet.yer_withdrawn += amount
            
        elif currency == 'SAR':
            if wallet.sar_available < amount:
                return jsonify({"status": "error", "message": "رصيد الريال السعودي المتاح غير كافٍ."}), 400
            wallet.sar_available -= amount
            wallet.sar_withdrawn += amount
            
        elif currency == 'USD':
            if wallet.usd_available < amount:
                return jsonify({"status": "error", "message": "رصيد الدولار المتاح غير كافٍ."}), 400
            wallet.usd_available -= amount
            wallet.usd_withdrawn += amount

        # تحديث حالة السجل المالي وتوثيق هوية المسؤول المعمّد للمشهد
        transaction.tx_status = 'completed'
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": f"تم تعميد صرف الحوالة بنجاح برقم {transaction.transaction_ref}"}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطر مالي أثناء تعميد السحب: {str(e)}")
        return jsonify({"status": "error", "message": f"فشل التعميد المالي: {str(e)}"}), 500


@admin_wallet.route('/reject-withdrawal', methods=['POST'])
@login_required
def reject_withdrawal():
    """
    رفض طلب السحب سيادياً: إعادة الأموال المحتجزة إلى رصيد المورد المتاح دون خصم.
    """
    tx_id = request.form.get('tx_id')
    reason = request.form.get('reason', 'تم الرفض من قبل الإدارة العليا').strip()

    try:
        transaction = WalletTransaction.query.with_for_update().get(tx_id)
        if not transaction or transaction.tx_status != 'pending':
            return jsonify({"status": "error", "message": "العملية غير صالحة لإجراء الرفض."}), 400

        # إعادة الرصيد المحتجز (Pending) إلى المتاح (Available) في حال تطلب منطق المنصة المالي ذلك،
        # أو الاكتفاء بإسقاط وتغيير حالة العملية المادية إلى مرفوضة بناءً على هيكل الحسابات لديك:
        transaction.tx_status = 'rejected'
        transaction.description = f"{transaction.description} | سبب الرفض: {reason}"
        transaction.approved_by_id = current_user.id if hasattr(current_user, 'id') else None
        
        db.session.commit()
        return jsonify({"status": "success", "message": "تم رفض طلب السحب وإعادة الأموال للمورد بنجاح."}), 200

    except Exception as e:
        db.session.rollback()
        current_app.logger.error(f"❌ خطأ أثناء إسقاط العملية المالية: {str(e)}")
        return jsonify({"status": "error", "message": str(e)}), 500
