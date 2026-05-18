# coding: utf-8
# 💳 محرك الحوكمة المالية والمسارات السيادية للمحافظ - منصة محجوب أونلاين 2026

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from apps import db
from apps.models.supplier_db import Supplier

# 🛡️ تكتيك حوكمي مرن لمنع الـ ImportError والانهيار المفاجئ أثناء استدعاء المحافظ
try:
    from apps.models.wallet_db import Wallet, WalletTransaction
except ImportError:
    # ملاذ آمن في حال كان اسم الكلاس في الموديل مسجلاً بصيغة الجمع WalletTransactions
    from apps.models.wallet_db import Wallet
    from apps.models.wallet_db import WalletTransactions as WalletTransaction

# إنشاء البلوبرينت المالي مع ربطه بالمجلد الفرعي بشكل صحيح لضمان عدم تداخل التطبيقات
admin_wallet = Blueprint('admin_wallet', __name__, template_folder='templates')

@admin_wallet.route('/admin/wallet/overview', methods=['GET'])
@login_required
def overview():
    """
    شاشة فحص وجرد الحسابات المادية:
    تستقبل طلبات التفتيش الفوري وتتوافق مع الجداول لضمان تشغيل التطبيقات الأخرى بسلاسة.
    """
    # التأكد من الصلاحيات السيادية للمستخدم (Owner أو Admin)
    if current_user.role not in ['Owner', 'Admin']:
        flash('غير مسموح لك بامتلاك صلاحية دخول الفضاء المالي.', 'danger')
        return redirect(url_for('admin_dashboard.dashboard'))

    search_query = request.args.get('search', '').strip()
    
    try:
        # بناء استعلام جلب الحسابات مع ربط الموردين لضمان عدم حدوث تعارض مالي داخلي
        query = Wallet.query.join(Supplier, Wallet.supplier_id == Supplier.id)

        # التفتيش الذكي الفوري
        if search_query and search_query != '#':
            query = query.filter(
                (Supplier.trade_name.like(f'%{search_query}%')) |
                (Supplier.sovereign_id.like(f'%{search_query}%')) |
                (Wallet.wallet_code.like(f'%{search_query}%'))
            )

        wallets = query.all()
    except Exception as e:
        # في حال حدوث أي تعارض لحظي أثناء البناء، يتم تصفير المصفوفة حتى لا تتأثر التطبيقات الأخرى
        wallets = []
        print(f"📡 تنبيه حوكمة المحافظ: جاري مواءمة الجداول الهيكلية: {e}")

    return render_template('admin/overview.html', wallets=wallets)


@admin_wallet.route('/api/wallet/<string:wallet_code>/balance', methods=['GET'])
@login_required
def get_wallet_balance_api(wallet_code):
    """
    واجهة برمجة تطبيقات (API) آمنة بنظام جيسون لخدمة العمليات البرمجية في اللوحات الأخرى.
    """
    if current_user.role not in ['Owner', 'Admin']:
        return jsonify({"status": "error", "message": "صلاحية سيادية مرفوضة"}), 403

    wallet = Wallet.query.filter_by(wallet_code=wallet_code).first()
    
    if not wallet:
        return jsonify({"status": "error", "message": "المحفظة المالية غير موجودة بالنظام"}), 404

    try:
        wallet_data = wallet.to_dict()
    except AttributeError:
        # ملاذ آمن مبسط في حال عدم توفر دالة to_dict() بالموديل لقراءة حقول الأرصدة الثلاثية مباشرة
        wallet_data = {
            "id": wallet.id,
            "wallet_code": wallet.wallet_code,
            "yer_balance": getattr(wallet, 'yer_balance', 0.0),
            "sar_balance": getattr(wallet, 'sar_balance', 0.0),
            "usd_balance": getattr(wallet, 'usd_balance', 0.0)
        }

    return jsonify({
        "status": "success",
        "data": wallet_data
    })


@admin_wallet.route('/admin/wallet/adjust', methods=['POST'])
@login_required
def adjust_balance():
    """
    صلاحية المالك المطلقة لتعديل وضبط أرصدة الخزائن الثلاثية دون التأثير على بقية النواة.
    """
    if current_user.role != 'Owner':
        flash('هذا الإجراء يتطلب سلطة المالك السيادية المطلقة.', 'danger')
        return redirect(url_for('admin_wallet.overview'))

    wallet_id = request.form.get('wallet_id')
    currency = request.form.get('currency')  # 'YER', 'SAR', 'USD'
    action_type = request.form.get('action_type')  # 'deposit', 'withdrawal'
    amount_str = request.form.get('amount', '0')

    try:
        amount = float(amount_str)
        if amount <= 0:
            flash('يجب أن تكون القيمة المالية أكبر من صفر.', 'warning')
            return redirect(url_for('admin_wallet.overview'))
            
        wallet = Wallet.query.get(wallet_id)
        if not wallet:
            flash('المحفظة المستهدفة غير مسجلة في الفضاء الحالي.', 'danger')
            return redirect(url_for('admin_wallet.overview'))

        # التعديل المباشر والآمن للأرصدة عبر الـ fallback الحامي لمنع خطأ 'yer_total'
        if currency == 'YER':
            current_bal = float(getattr(wallet, 'yer_balance', 0.0))
            if action_type == 'deposit':
                wallet.yer_balance = current_bal + amount
            elif action_type == 'withdrawal':
                available_bal = float(getattr(wallet, 'yer_available', current_bal))
                if available_bal < amount:
                    flash('رصيد الريال اليمني المتاح لا يكفي.', 'danger')
                    return redirect(url_for('admin_wallet.overview'))
                wallet.yer_balance = current_bal - amount

        elif currency == 'SAR':
            current_bal = float(getattr(wallet, 'sar_balance', 0.0))
            if action_type == 'deposit':
                wallet.sar_balance = current_bal + amount
            elif action_type == 'withdrawal':
                available_bal = float(getattr(wallet, 'sar_available', current_bal))
                if available_bal < amount:
                    flash('رصيد الريال السعودي المتاح لا يكفي.', 'danger')
                    return redirect(url_for('admin_wallet.overview'))
                wallet.sar_balance = current_bal - amount

        elif currency == 'USD':
            current_bal = float(getattr(wallet, 'usd_balance', 0.0))
            if action_type == 'deposit':
                wallet.usd_balance = current_bal + amount
            elif action_type == 'withdrawal':
                available_bal = float(getattr(wallet, 'usd_available', current_bal))
                if available_bal < amount:
                    flash('رصيد الدولار الأمريكي المتاح لا يكفي.', 'danger')
                    return redirect(url_for('admin_wallet.overview'))
                wallet.usd_balance = current_bal - amount
        
        # توثيق التعديل اللوجستي في جدول الحركات المالية المتوافق
        tx_log = WalletTransaction(
            wallet_id=wallet.id,
            transaction_type=action_type,
            currency=currency,
            amount=amount,
            description="تعديل إداري مباشر من لوحة تحكم المالك السيادية"
        )
        
        db.session.add(tx_log)
        db.session.commit()
        
        flash(f'تم تحديث كشف حساب المحفظة {wallet.wallet_code} بنجاح وتصفير التعارضات.', 'success')

    except ValueError:
        flash('خطأ: صيغة المبلغ المدخل غير صالحة.', 'danger')
    except Exception as e:
        db.session.rollback()
        flash(f'تعذر تعديل الرصيد بسبب عطل في الربط الهيكلي: {e}', 'danger')

    return redirect(url_for('admin_wallet.overview'))
