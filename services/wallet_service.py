import uuid
import random
import string

def generate_wallet_id(next_id):
    """
    توليد رقم محفظة سيادي مرتبط مباشرة بالهوية السيادية للمورد.
    بدلاً من العشوائية، نعتمد الآن الربط المباشر: W- + المعرف المولد.
    الناتج المتوقع: W-MAH-9631
    """
    # الربط المباشر لضمان وحدة الهوية الرقمية والمالية
    wallet_id = f"W-{next_id}"
    
    return wallet_id

def validate_wallet_balance(vendor):
    """
    التحقق من جاهزية أرصدة المورد قبل أي عملية تعميد مالي لضمان استقرار النظام.
    تدعم الترسانة العملات الثلاث المعتمدة في اليمن (ريال يمني، سعودي، دولار).
    """
    balances = {
        'YER': getattr(vendor, 'balance_yer', 0.0) or 0.0,
        'SAR': getattr(vendor, 'balance_sar', 0.0) or 0.0,
        'USD': getattr(vendor, 'balance_usd', 0.0) or 0.0
    }
    return balances

def format_currency(amount, currency="YER"):
    """
    تنسيق المبالغ المالية لتظهر بشكل لائق واحترافي في واجهات محجوب أونلاين.
    """
    try:
        amount = float(amount)
    except (ValueError, TypeError):
        amount = 0.0

    if currency == "YER":
        return f"{amount:,.0f} ريال يمني"
    elif currency == "SAR":
        return f"{amount:,.2f} ريال سعودي"
    elif currency == "USD":
        return f"{amount:,.2f} دولار"
    return f"{amount:,.2f} {currency}"

def process_sovereign_commission(amount, rate=0.01):
    """
    حساب عمولة المنصة (عقل المحفظة السيادي).
    افتراضياً 1% أو حسب الاتفاقية مع المورد.
    """
    return amount * rate

def log_financial_transaction(db, transaction_model, vendor_id, amount, currency, action_type, note=""):
    """
    أرشفة التحركات المالية في السجل العام للترسانة لضمان الشفافية والحوكمة.
    """
    try:
        new_tx = transaction_model(
            vendor_id=vendor_id,
            amount=amount,
            currency=currency,
            action_type=action_type,
            note=note
        )
        db.session.add(new_tx)
        # لا نقوم بعمل commit هنا، بل نتركها للدالة الأم لضمان وحدة العملية (Atomicity)
        return True
    except Exception as e:
        print(f"⚠️ خطأ في أرشفة العملية المالية: {e}")
        return False
