import uuid
import random
import string

def generate_wallet_id(prefix="W-MAH-"):
    """
    توليد رقم محفظة سيادي فريد لمنصة محجوب أونلاين.
    مثال الناتج: W-MAH-9631
    """
    # توليد 4 أرقام عشوائية لضمان التميز
    random_digits = ''.join(random.choices(string.digits, k=4))
    
    # دمج البادئة مع الأرقام
    wallet_id = f"{prefix}{random_digits}"
    
    return wallet_id

def validate_wallet_balance(vendor):
    """
    التحقق من جاهزية أرصدة المورد قبل أي عملية تعميد مالي.
    """
    balances = {
        'YER': vendor.balance_yer or 0.0,
        'SAR': vendor.balance_sar or 0.0,
        'USD': vendor.balance_usd or 0.0
    }
    return balances

# يمكنك إضافة دوال إضافية هنا لاحقاً مثل (تحويل الرصيد، خصم عمولة، إلخ)
