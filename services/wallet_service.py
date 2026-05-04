import uuid
from decimal import Decimal

class WalletService:
    @staticmethod
    def generate_wallet_id(next_id):
        """توليد رقم محفظة سيادي مرتبط بالهوية الرقمية (مثال: W-MAH-9631)"""
        return f"W-{next_id}"

    @staticmethod
    def validate_wallet_balance(vendor):
        """التحقق من جاهزية الأرصدة للعملات الثلاث المعتمدة في اليمن"""
        return {
            'YER': getattr(vendor, 'balance_yer', 0.0) or 0.0,
            'SAR': getattr(vendor, 'balance_sar', 0.0) or 0.0,
            'USD': getattr(vendor, 'balance_usd', 0.0) or 0.0
        }

    @staticmethod
    def format_currency(amount, currency="YER"):
        """تنسيق احترافي للمبالغ المالية حسب نوع العملة"""
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

    @staticmethod
    def log_financial_transaction(db, transaction_model, vendor_id, amount, currency, action_type, note=""):
        """أرشفة التحركات المالية لضمان الشفافية والحوكمة المركزية"""
        try:
            new_tx = transaction_model(
                vendor_id=vendor_id,
                amount=amount,
                currency=currency,
                action_type=action_type,
                note=note
            )
            db.session.add(new_tx)
            return True
        except Exception as e:
            print(f"⚠️ خطأ في أرشفة العملية المالية: {e}")
            return False
